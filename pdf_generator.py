# pdf_generator.py
# PDF generation and Google Drive upload functionality

import streamlit as st
import io
import datetime
from pdfrw import PdfObject, PdfName, PdfReader, PdfWriter
import fitz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image
import numpy as np
import base64
from config import PDF_FOLDER_ID
from sheets_manager import get_service_account_info_from_secrets


def get_drive_service():
    sa_info = get_service_account_info_from_secrets()
    creds = Credentials.from_service_account_info(sa_info, scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)
    return service


def sanitize_for_pdf(value):
    if not isinstance(value, str):
        value = str(value)
    return (
        value.replace("(", "[")
             .replace(")", "]")
             .replace("&", "and")
             .replace("\n", " / ")
             .replace("\r", "")
             .replace(":", "-")
             .replace("\"", "'")
             .replace("\\", "/")
             .strip()
    )


def generate_pdf(plants_data, installation_data, customer_data, pricing_data, customer_signature=None):
    try:
        template_path = "install_template.pdf"
        filled_path = "/tmp/filled_temp.pdf"
        output_buffer = io.BytesIO()

        ANNOT_KEY = "/Annots"
        ANNOT_FIELD_KEY = "/T"
        ANNOT_VAL_KEY = "/V"
        SUBTYPE_KEY = "/Subtype"
        WIDGET_SUBTYPE_KEY = "/Widget"

        total_number_of_plants = sum([p.get("quantity", 0) for p in plants_data.values()])
        tablet_total_quantity = pricing_data.get("tablet_total_quantity", 0)
        mulch_total_quantity = pricing_data.get("mulch_total_quantity", 0)
        soil_conditioner_total_quantity = pricing_data.get("soil_conditioner_total_quantity", 0)

        tablet_total_price = pricing_data.get("tablet_total_price", 0)
        mulch_total_price = pricing_data.get("mulch_total_price", 0)
        soil_conditioner_total_price = pricing_data.get("soil_conditioner_total_price", 0)
        deer_guard_price = pricing_data.get("deer_guard_price", 0)
        tree_stakes_price = pricing_data.get("tree_stakes_price", 0)
        mulch_sku = pricing_data.get("mulch_sku", 0)

        now = datetime.datetime.now()
        date_sold = f"{now.month}/{now.day}/{now.year}"

        installation_cost = pricing_data.get("installation_cost", 0)

        all_materials_discount_total = (
            pricing_data.get("plant_material_discount_total", 0)
            + pricing_data.get("installation_material_total", 0)
        )

        planting_costs_total = (
            pricing_data.get("installation_cost", 0)
            + pricing_data.get("delivery_cost", 0)
        )

        data = {
            "customer_name": customer_data.get("customer_name", ""),
            "customer_email": customer_data.get("customer_email", ""),
            "customer_phone": customer_data.get("customer_phone", ""),
            "customer_street_address": installation_data.get('customer_street_address', ''),
            "customer_city": installation_data.get('customer_city', ''),
            "customer_zip": installation_data.get('customer_zip', ''),
            "customer_subdivision": customer_data.get("customer_subdivision", ""),
            "customer_cross_street": customer_data.get("customer_cross_street", ""),
            "gate_response": customer_data.get("gate_response", ""),
            "gate_width": customer_data.get("gate_width", ""),
            "dogs_response": customer_data.get("dogs_response", ""),
            "install_location": customer_data.get("install_location", ""),
            "utilities_check": " / ".join(customer_data.get("utilities_check", [])),
            "notes": customer_data.get("notes", ""),
            "employee_initials": customer_data.get("employee_initials", ""),
            "pos_customer_number": customer_data.get("customer_number", ""),
            "pos_order_number": customer_data.get("order_number", ""),
            "mulch_type": installation_data.get("mulch_type", ""),
            "tree_stakes_quantity": installation_data.get("tree_stakes_quantity", 0),
            "deer_guards_quantity": installation_data.get("deer_guards_quantity", 0),
            "installation_type": installation_data.get("installation_type", ""),
            "origin_location": installation_data.get("origin_location", ""),
            "plant_list": "\n".join([
                f"{p['quantity']} x {p['plant_material']} ({p['size']}) - ${p['price']:.2f}"
                + (f" ({p['discount_percent']}% off" if p.get('discount_percent') else "")
                + (f", ${p['discount_dollars']:.2f} off" if p.get('discount_dollars') else "")
                + (")" if p.get('discount_percent') or p.get('discount_dollars') else "")
                for p in plants_data.values()
            ]),
            "total_price": f"${pricing_data.get('final_total', 0):.2f}",
            "subtotal": f"${pricing_data.get('final_subtotal', 0):.2f}",
            "tax": f"${pricing_data.get('final_tax', 0):.2f}",
            "delivery_cost": f"${pricing_data.get('delivery_cost', 0):.2f}",
            "flag_quantity": total_number_of_plants,
            "total_tablet_quantity": tablet_total_quantity,
            "total_mulch_quantity": mulch_total_quantity,
            "mulch_sku": mulch_sku,
            "type_of_mulch": pricing_data.get('mulch_type', ''),
            "total_soil_conditioner_quantity": soil_conditioner_total_quantity,
            "tablet_total_price": f"${tablet_total_price:.2f}",
            "mulch_total_price": f"${mulch_total_price:.2f}",
            "soil_conditioner_total_price": f"${soil_conditioner_total_price:.2f}",
            "deer_guard_price": f"${deer_guard_price:.2f}",
            "tree_stakes_price": f"${tree_stakes_price:.2f}",
            "installation_cost": f"${installation_cost:.2f}",
            "all_materials_discount_total": f"${all_materials_discount_total:.2f}",
            "planting_costs_total": f"${planting_costs_total:.2f}",
            "date_sold": date_sold,
        }

        template_pdf = PdfReader(template_path)
        for page in template_pdf.pages:
            annotations = page.get(ANNOT_KEY)
            if annotations:
                for annotation in annotations:
                    if annotation.get(SUBTYPE_KEY) == WIDGET_SUBTYPE_KEY:
                        key = annotation.get(ANNOT_FIELD_KEY)
                        if key:
                            key_name = str(key)[1:-1] if not isinstance(key, str) else key.strip("()")
                            if key_name in data:
                                value = sanitize_for_pdf(data[key_name])
                                annotation[PdfName("V")] = PdfObject(f"({value})")

        PdfWriter(filled_path, trailer=template_pdf).write()

        doc = fitz.open(filled_path)
        
        signature_field_found = False
        signature_placed = False
        
        if customer_signature is not None:
            try:
                has_signature_content = False
                sig_bytes = None
                
                if hasattr(customer_signature, 'image_data'):
                    import numpy as np
                    img_data = customer_signature.image_data
                    
                    if img_data is not None and img_data.size > 0:
                        if np.any(img_data[:, :, 3] > 0):  # Check alpha channel for any marks
                            has_signature_content = True
                            sig_img = Image.fromarray(img_data.astype('uint8'), 'RGBA')
                            
                            sig_bytes = io.BytesIO()
                            sig_img.save(sig_bytes, format='PNG')
                            sig_bytes.seek(0)
                
                if has_signature_content and sig_bytes is not None:
                    for page_num, page in enumerate(doc):
                        widgets = page.widgets()
                        if widgets:
                            for widget in widgets:
                                if widget.field_name == "customer_signature":
                                    signature_field_found = True
                                    
                                    x0 = 7 * 72  # = 264.528
                                    y0 = 11 * 72  # = 674.0712
                                    width = 1.8783 * 72  # = 135.2376
                                    height = 0.6261 * 72  # = 45.0792
                                    
                                    adjusted_rect = fitz.Rect(
                                        x0,
                                        y0,
                                        x0 + width,
                                        y0 + height
                                    )
                                    
                                    if adjusted_rect and adjusted_rect.is_valid and not adjusted_rect.is_empty:
                                        page.insert_image(adjusted_rect, stream=sig_bytes.getvalue(), keep_proportion=True)
                                        signature_placed = True
                                        widget.field_flags |= 1 << 0
                                        widget.update()
                                        break
                            
                            if signature_placed:
                                break
                    
                    if not signature_placed:
                        page = doc[-1]
                        
                        rect = fitz.Rect(265, 684, 365, 719)
                        
                        if rect and rect.is_valid and not rect.is_empty:
                            page.insert_image(rect, stream=sig_bytes.getvalue(), keep_proportion=True)
                            signature_placed = True
                        else:
                            st.warning(f"Fallback rect is invalid")
                
            except Exception as e:
                st.warning(f"Could not add signature to PDF: {e}")
        
        for page in doc:
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    if signature_field_found and widget.field_name == "customer_signature":
                        continue
                    widget.update()
                    widget.field_flags |= 1 << 0  # Set ReadOnly
        
        doc.save(output_buffer, deflate=True)
        output_buffer.seek(0)

        return output_buffer

    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None


def upload_pdf_to_drive(pdf_buffer, filename, install_id=None):
    try:
        service = get_drive_service()
        
        if install_id:
            query = f"name contains '{install_id}' and '{PDF_FOLDER_ID}' in parents and trashed=false"
            results = service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                supportsAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            for file in files:
                # Delete the old file
                service.files().delete(fileId=file['id'], supportsAllDrives=True).execute()

        file_metadata = {
            "name": filename,
            "parents": [PDF_FOLDER_ID]
        }

        media = MediaIoBaseUpload(pdf_buffer, mimetype="application/pdf", resumable=True)

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id",
            supportsAllDrives=True
        ).execute()

        file_id = uploaded_file.get("id")

        return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

    except Exception as e:
        st.error(f"Error uploading PDF to Drive: {e}")
        return ""