import os


REPORT_DIR = "knowledge_graph/corrected_reports_v2"


bad = []
empty = []
count = 0


for file in os.listdir(REPORT_DIR):

    if not file.endswith(".txt"):
        continue

    count += 1

    path = os.path.join(
        REPORT_DIR,
        file
    )

    with open(path) as f:
        text = f.read().strip()


    if len(text) < 30:
        empty.append(file)


    if (
        "Possible missing findings" in text
        or text.endswith("No .")
    ):
        bad.append(file)



print("="*60)
print("CORRECTED REPORT QUALITY CHECK")
print("="*60)

print("Total reports:", count)
print("Empty/short reports:", len(empty))
print("Bad formatting reports:", len(bad))


if empty:
    print("\nShort reports:")
    print(empty[:10])


if bad:
    print("\nBad reports:")
    print(bad[:10])

print("="*60)
