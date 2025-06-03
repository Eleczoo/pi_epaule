"""
This is a simple class that can create a PDF report using typst

It can add:
- Title
- Paragraphs
- Image
- Table
- List

"""

import os
import shutil

import cv2 as cv
import typst


class ReportCreator:
    def __init__(
        self,
        report_temp_dir: str,
        template_dir: str,
        report_output_pdf: str,
    ):
        """
        Utility to create a PDF report using typst

        Args:
        - report_temp_dir: Directory where a temporary report will be created
        - template_dir: Directory where the template files are stored
        - report_output_pdf: Full path where you want the PDF report to be saved at
        """
        self.report_temp_dir = report_temp_dir
        self.template_dir = template_dir
        self.report_output_pdf = report_output_pdf

        self.create_report()

        # This will contain a list of lines
        # that will be added to the report
        # as content
        self.content = []

    def create_report(self):
        """
        This will create a base typst file for the report
        """
        # Create directoy for output
        os.makedirs(self.report_temp_dir, exist_ok=True)

        # Copy the template conf.typ file and main.typ file
        shutil.copy(os.path.join(self.template_dir, "conf.typ"), os.path.join(self.report_temp_dir, "conf.typ"))
        shutil.copy(os.path.join(self.template_dir, "main.typ"), os.path.join(self.report_temp_dir, "main.typ"))

    def add_list(self, data: list):
        """
        This will add a list to the report
        """
        for item in data:
            self.content.append(f"- {item}")

    def add_title(self, title: str):
        """
        This will add a title to the report
        """
        self.content.append(f"= {title}")

    def add_subtitle(self, subtitle: str, level: int = 2):
        """
        This will add a subtitle to the report
        """
        self.content.append(f"{'=' * level} {subtitle}")

    def add_ordered_list(self, data: list):
        """
        This will add an ordered list to the report
        """
        for item in data:
            self.content.append(f"+ {item}")

    def add_paragraphs(self, paragraph: list[str]):
        """
        This will add a paragraph to the report
        """
        if isinstance(paragraph, list):
            for p in paragraph:
                self.add_paragraph(p)

    def add_paragraph(self, paragraph: str):
        """
        This will add a paragraph to the report
        """
        self.content.append(f"{paragraph}")

    def add_image(self, image_path: str, caption: str):
        """
        This will add an image to the report
        """
        img = f'''
#figure(
  image("{image_path}", width: 100%),
  caption: [
		{caption}
    ],
)
'''
        self.content.append(img)

    def save_image(self, filename: str, image_data: cv.Mat):
        """
        This will save an image to the report_temp_dir
        """

        # Save the image to the report_temp_dir
        cv.imwrite(os.path.join(self.report_temp_dir, filename), image_data)

        return filename

    def add_box(self, title: str, body: str, footer: str):
        """
        This will add a box to the report
        """
        box = f"""
#redbox(
    [{title}],
    "{body}",
    "{footer}"
)
"""

        self.content.append(box)

    def add_pagebreak(self):
        """
        This will add a pagebreak to the report
        """
        self.content.append("#pagebreak()")

    def compile_report(self):
        """
        This will compile the final report
        """
        # Add the content to the main.typ file
        with open(f"{self.report_temp_dir}/main.typ", "a", encoding="utf-8") as f:
            for line in self.content:
                f.write(f"{line}\n")

        typst.compile(
            f"{self.report_temp_dir}/main.typ",
            f"{self.report_output_pdf}",
        )


if __name__ == "__main__":
    template_dir = "report_template"
    report_temp_dir = "report_temp_dir"

    report_creator = ReportCreator(
        template_dir=template_dir,
        report_temp_dir=report_temp_dir,
        report_output_pdf="report.pdf",
    )

    # Copy the template image into the report_temp_dir
    shutil.copy(os.path.join(template_dir, "test_image.svg"), os.path.join(report_temp_dir, "test_image.svg"))

    report_creator.add_title("Test Report")
    report_creator.add_subtitle("Test subtitle")
    report_creator.add_paragraph("This is a test paragraph")
    report_creator.add_image(
        image_path="./test_image.svg",
        caption="This is a test image",
    )
    report_creator.add_pagebreak()
    report_creator.add_list(["item1", "item2", "item3"])
    report_creator.add_ordered_list(["item1", "item2", "item3"])
    # report_creator.add_box(
    #     title="Test box",
    #     body="This is the body",
    #     footer="This is the footer",
    # )

    report_creator.compile_report()

    print(f"Report created at {report_creator.report_output_pdf}")
