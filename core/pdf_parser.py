import fitz
import os


class PDFParser:

    def pdf_to_images(self,
                      pdf_path,
                      output_dir,
                      scale=5):

        os.makedirs(output_dir, exist_ok=True)

        doc = fitz.open(pdf_path)

        image_paths = []

        for page_index in range(len(doc)):

            page = doc[page_index]

            mat = fitz.Matrix(scale, scale)

            pix = page.get_pixmap(matrix=mat)

            out_path = os.path.join(
                output_dir,
                f"page_{page_index + 1}.png"
            )

            pix.save(out_path)

            image_paths.append(out_path)

            print(f"PDF转图片: {out_path}")

        doc.close()

        return image_paths