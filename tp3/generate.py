from pathlib import Path
import subprocess
from jinja2 import Template

template = Template(
    Path("experiment.java.jinja").read_text()
)

properties = {
    "associativity": (
        "(x + y) + z",
        "x + (y + z)"
    ),

    "distributivity": (
        "x * (y + z)",
        "x * y + x * z"
    )
}

types = ["float", "double"]

output_dir = Path("generated")
output_dir.mkdir(exist_ok=True)

for property_name, (lhs, rhs) in properties.items():

    for number_type in types:

        class_name = (
            property_name.capitalize() +
            number_type.capitalize()
        )

        code = template.render(
            class_name=class_name,
            property_name=property_name,
            type=number_type,
            lhs=lhs,
            rhs=rhs
        )

        java_file = output_dir / f"{class_name}.java"

        java_file.write_text(code)

        # Compile the generated Java program
        subprocess.run(
            ["javac", "-d", str(output_dir), str(java_file)],
            check=True
        )

        # Execute the generated program
        result = subprocess.run(
            ["java", "-cp", str(output_dir), class_name],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout.strip())