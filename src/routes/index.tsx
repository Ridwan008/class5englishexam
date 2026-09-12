import { createFileRoute } from "@tanstack/react-router";
import { Download, FileText, Printer, Smartphone, Monitor, FolderArchive } from "lucide-react";
import type { ReactNode } from "react";

export const Route = createFileRoute("/")({ component: Home });

const FILES = {
  editDocx: "/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.docx",
  printPdf: "/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.pdf",
  apk: "/downloads/Class5-English-SMT04.apk",
  exe: "/downloads/Class5-English-SMT04.exe",
  zip: "/downloads/Class5-English-SMT04-offline.zip",
};

const PAGES = [
  { n: 1, label: "Q.1 – Q.3  ·  Farhana's field trip", src: "/preview/page-1.png" },
  { n: 2, label: "Q.4 – Q.10  ·  Roni, grammar, paragraph, letter", src: "/preview/page-2.png" },
];

function Home() {
  return (
    <main className="min-h-screen">
      <header className="border-b-4 border-[#c9a227] bg-[#7f1d1d] text-[#faf6ee]">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-5 sm:flex-row sm:items-end sm:justify-between sm:px-6">
          <div>
            <p className="text-[11px] font-semibold tracking-[0.22em] text-[#e8c547] uppercase">
              Rabeya Coaching Center
            </p>
            <h1
              className="mt-1 text-2xl font-bold leading-tight sm:text-3xl"
              style={{ fontFamily: '"Source Serif 4", Georgia, serif' }}
            >
              Class Five English
            </h1>
            <p className="mt-1 text-sm text-[#f3d9a4]">
              Special Model Test 04 · Second Terminal Examination · 70 marks · 2 hours 30 minutes
            </p>
          </div>
          <p className="max-w-sm text-xs leading-relaxed text-[#f0d7b0] sm:text-right">
            A4, 2 page, fully offline. Android APK, Windows EXE, Word ar PDF — internet chara kaj kore.
          </p>
        </div>
      </header>

      <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
        <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <DownloadCard
            href={FILES.apk}
            icon={<Smartphone className="size-5" />}
            title="Android APK — offline"
            sub="Phone e install koro. Internet lage na. Paper, Word, PDF app-er vitore."
            cta="Download .apk"
            primary
          />
          <DownloadCard
            href={FILES.exe}
            icon={<Monitor className="size-5" />}
            title="Windows EXE — offline"
            sub="Double-click korle browser e paper khulbe. Internet lage na."
            cta="Download .exe"
          />
          <DownloadCard
            href={FILES.zip}
            icon={<FolderArchive className="size-5" />}
            title="Offline ZIP — sob file"
            sub="index.html, exam paper, Word, PDF, source — ekta zip e."
            cta="Download .zip"
          />
          <DownloadCard
            href={FILES.editDocx}
            icon={<FileText className="size-5" />}
            title="Word file — edit kora jabe"
            sub="A4, 2 page, unlocked. Word / Google Docs / WPS e khule change koro."
            cta="Download .docx"
          />
          <DownloadCard
            href={FILES.printPdf}
            icon={<Printer className="size-5" />}
            title="Print PDF — A4, 2 page"
            sub="A4 portrait. Fold korte hobe na. Shop e bolo: A4, 2 page print."
            cta="Download PDF"
          />
        </section>

        <section className="mt-8 rounded-2xl border border-[#e0d4c0] bg-white p-5 shadow-sm sm:p-6">
          <h2
            className="text-lg font-bold text-[#7f1d1d]"
            style={{ fontFamily: '"Source Serif 4", Georgia, serif' }}
          >
            Kivabe edit & print
          </h2>
          <ol className="mt-3 grid gap-3 text-sm leading-relaxed text-[#3f3a34] sm:grid-cols-3">
            <Step n="1" title="Word download">
              .docx ta download koro. PC te <strong>Microsoft Word</strong> ba phone e{" "}
              <strong>Google Docs / WPS</strong> diye khulo — Read-only thakbe na.
            </Step>
            <Step n="2" title="Ja iccha edit">
              Header, passage, question, marks — shob normal text. Type koro, delete koro, save koro.
            </Step>
            <Step n="3" title="A4 print">
              Paper size <strong>A4</strong>, portrait, 2 page. Shop e bolo: “A4, 2 page print”.
            </Step>
          </ol>
        </section>

        <section className="mt-8">
          <div className="mb-3 flex items-end justify-between gap-3">
            <h2
              className="text-lg font-bold text-[#7f1d1d]"
              style={{ fontFamily: '"Source Serif 4", Georgia, serif' }}
            >
              Question paper — 2 pages (A4)
            </h2>
            <a
              href="/exam.html"
              target="_blank"
              rel="noreferrer"
              className="text-sm font-semibold text-[#7f1d1d] underline-offset-2 hover:underline"
            >
              Full size preview
            </a>
          </div>
          <div className="grid gap-4 lg:grid-cols-2">
            {PAGES.map((p) => (
              <article
                key={p.n}
                className="overflow-hidden rounded-xl border border-[#e0d4c0] bg-white shadow-sm"
              >
                <div className="flex items-center justify-between border-b border-[#efe6d6] bg-[#faf6ee] px-3 py-2">
                  <p className="text-sm font-bold text-[#7f1d1d]">
                    Page {p.n}
                    <span className="ml-2 font-medium text-[#5c5348]">{p.label}</span>
                  </p>
                </div>
                <a href={p.src} target="_blank" rel="noreferrer">
                  <img src={p.src} alt={`Exam page ${p.n}`} className="block w-full bg-[#ddd2c0]" />
                </a>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-8 mb-10 rounded-2xl border border-[#e0d4c0] bg-[#fffdf8] p-5 text-sm leading-relaxed text-[#3f3a34] sm:p-6">
          <h2
            className="text-lg font-bold text-[#7f1d1d]"
            style={{ fontFamily: '"Source Serif 4", Georgia, serif' }}
          >
            Paper e ja ache
          </h2>
          <ul className="mt-3 grid gap-1.5 sm:grid-cols-2">
            <li>Page 1 — Passage (Liberation War Museum) + Q.1 MCQ/True-False + Q.2–3</li>
            <li>Page 2 — Roni’s garden Q.4–5, rearrange Q.6, grammar Q.7, verbs Q.8</li>
            <li>Q.9 Paragraph — Necessity of Eating Healthy Food (Unit 12)</li>
            <li>Q.10 Letter — Asif to Belal, annual sports day</li>
            <li>Full marks 70 · Time 2 hours 30 minutes · A4 × 2 pages</li>
          </ul>
        </section>
      </div>
    </main>
  );
}

function DownloadCard({
  href,
  icon,
  title,
  sub,
  cta,
  primary,
}: {
  href: string;
  icon: ReactNode;
  title: string;
  sub: string;
  cta: string;
  primary?: boolean;
}) {
  return (
    <a
      href={href}
      download
      className={
        "group flex flex-col rounded-2xl border p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md " +
        (primary
          ? "border-[#7f1d1d] bg-[#7f1d1d] text-[#faf6ee]"
          : "border-[#e0d4c0] bg-white text-[#1c1917]")
      }
    >
      <div
        className={
          "mb-3 inline-flex size-9 items-center justify-center rounded-full " +
          (primary ? "bg-[#c9a227] text-[#4c1010]" : "bg-[#faf6ee] text-[#7f1d1d]")
        }
      >
        {icon}
      </div>
      <h3 className="text-[15px] font-bold leading-snug">{title}</h3>
      <p className={"mt-1 flex-1 text-xs leading-relaxed " + (primary ? "text-[#f0d7b0]" : "text-[#5c5348]")}>
        {sub}
      </p>
      <span
        className={
          "mt-3 inline-flex items-center gap-1.5 text-sm font-semibold " +
          (primary ? "text-[#e8c547]" : "text-[#7f1d1d]")
        }
      >
        <Download className="size-4" />
        {cta}
      </span>
    </a>
  );
}

function Step({ n, title, children }: { n: string; title: string; children: ReactNode }) {
  return (
    <li className="rounded-xl bg-[#faf6ee] p-3">
      <p className="text-[11px] font-bold tracking-wider text-[#c9a227] uppercase">Step {n}</p>
      <p className="mt-0.5 font-bold text-[#7f1d1d]">{title}</p>
      <p className="mt-1 text-[13px]">{children}</p>
    </li>
  );
}
