"""Extract text from the reference PDFs (page-marked) for glossary mining."""
import sys, os, time
import PyPDF2

def extract(pdf_path, out_path):
    t0 = time.time()
    try:
        reader = PyPDF2.PdfReader(pdf_path)
    except Exception as e:
        print(f"  cannot open: {e}")
        return False
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as e:
            print(f"  decrypt failed: {e}")
            return False
    n = len(reader.pages)
    print(f"  pages: {n}")
    chunks = []
    for i in range(n):
        try:
            txt = reader.pages[i].extract_text() or ""
        except Exception:
            txt = ""
        chunks.append(f"\n<<<PAGE {i+1}>>>\n{txt}")
        if (i + 1) % 100 == 0:
            print(f"    {i+1}/{n} pages ({time.time()-t0:.0f}s)")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(chunks))
    print(f"  wrote {out_path} ({os.path.getsize(out_path)/1024/1024:.1f} MB, {time.time()-t0:.0f}s)")
    return True

if __name__ == "__main__":
    jobs = [
        (r"C:\Users\Khumza\.dsh\attachments\v1\files\1e\1e07c2720541a548fc8d960c06d6d6080f4da048c1b5243b7cea24fb9c31b4d0\Chapple M.  ISC2 CISSP Certified Information Systems...Study Guide 10ed 2024.pdf",
         r"C:\Users\Khumza\Documents\Coding projects\CISSP\_books\osg10.txt"),
        (r"C:\Users\Khumza\.dsh\attachments\v1\files\4f\4fa81d5f2e6304c19c836fa0ab29e6f66899f987ff611e6056542a43c7079e17\CISSP Exam Certification Companion. 1000+ Practice Questions...Strategies 2024.pdf",
         r"C:\Users\Khumza\Documents\Coding projects\CISSP\_books\companion.txt"),
    ]
    os.makedirs(r"C:\Users\Khumza\Documents\Coding projects\CISSP\_books", exist_ok=True)
    for pdf, out in jobs:
        print(f"\n=== {os.path.basename(pdf)[:60]} ===")
        if os.path.exists(out):
            print(f"  already extracted -> {out}")
            continue
        extract(pdf, out)
    print("\ndone")
