import { v as require_jsx_runtime } from "../_libs/@tanstack/react-router+[...].mjs";
import { i as Download, n as Printer, r as FileText } from "../_libs/lucide-react.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-DUhsAmSq.js
var import_jsx_runtime = require_jsx_runtime();
var FILES = {
	editDocx: "/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.docx",
	printPdf: "/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.pdf"
};
var PAGES = [{
	n: 1,
	label: "Q.1 – Q.3  ·  Farhana's field trip",
	src: "/preview/page-1.png"
}, {
	n: 2,
	label: "Q.4 – Q.10  ·  Roni, grammar, paragraph, letter",
	src: "/preview/page-2.png"
}];
function Home() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("main", {
		className: "min-h-screen",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("header", {
			className: "border-b-4 border-[#c9a227] bg-[#7f1d1d] text-[#faf6ee]",
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mx-auto flex max-w-6xl flex-col gap-3 px-4 py-5 sm:flex-row sm:items-end sm:justify-between sm:px-6",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "text-[11px] font-semibold tracking-[0.22em] text-[#e8c547] uppercase",
						children: "Rabeya Coaching Center"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-1 text-2xl font-bold leading-tight sm:text-3xl",
						style: { fontFamily: "\"Source Serif 4\", Georgia, serif" },
						children: "Class Five English"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-1 text-sm text-[#f3d9a4]",
						children: "Special Model Test 04 · Second Terminal Examination · 70 marks · 2 hours 30 minutes"
					})
				] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "max-w-sm text-xs leading-relaxed text-[#f0d7b0] sm:text-right",
					children: "A4 size, 2 page. Word file fully editable — lock nai. Print hole A4 portrait, 2 page."
				})]
			})
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "mx-auto max-w-6xl px-4 py-6 sm:px-6",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
					className: "grid gap-3 sm:grid-cols-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(DownloadCard, {
						href: FILES.editDocx,
						icon: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(FileText, { className: "size-5" }),
						title: "Word file — edit kora jabe",
						sub: "A4, 2 page, unlocked. Word / Google Docs / WPS e khule text, mark, kichu change koro.",
						cta: "Download .docx",
						primary: true
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DownloadCard, {
						href: FILES.printPdf,
						icon: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Printer, { className: "size-5" }),
						title: "Print PDF — A4, 2 page",
						sub: "A4 portrait. 2 page print. Fold korte hobe na. Photocopy shop-e A4 2 page dilei hoy.",
						cta: "Download PDF"
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
					className: "mt-8 rounded-2xl border border-[#e0d4c0] bg-white p-5 shadow-sm sm:p-6",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
						className: "text-lg font-bold text-[#7f1d1d]",
						style: { fontFamily: "\"Source Serif 4\", Georgia, serif" },
						children: "Kivabe edit & print"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("ol", {
						className: "mt-3 grid gap-3 text-sm leading-relaxed text-[#3f3a34] sm:grid-cols-3",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Step, {
								n: "1",
								title: "Word download",
								children: [
									".docx ta download koro. PC te ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Microsoft Word" }),
									" ba phone e",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Google Docs / WPS" }),
									" diye khulo — Read-only thakbe na."
								]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Step, {
								n: "2",
								title: "Ja iccha edit",
								children: "Header, passage, question, marks — shob normal text. Type koro, delete koro, save koro."
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Step, {
								n: "3",
								title: "A4 print",
								children: [
									"Paper size ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "A4" }),
									", portrait, 2 page. Shop e bolo: “A4, 2 page print”."
								]
							})
						]
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
					className: "mt-8",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mb-3 flex items-end justify-between gap-3",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
							className: "text-lg font-bold text-[#7f1d1d]",
							style: { fontFamily: "\"Source Serif 4\", Georgia, serif" },
							children: "Question paper — 2 pages (A4)"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
							href: "/exam.html",
							target: "_blank",
							rel: "noreferrer",
							className: "text-sm font-semibold text-[#7f1d1d] underline-offset-2 hover:underline",
							children: "Full size preview"
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "grid gap-4 lg:grid-cols-2",
						children: PAGES.map((p) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("article", {
							className: "overflow-hidden rounded-xl border border-[#e0d4c0] bg-white shadow-sm",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "flex items-center justify-between border-b border-[#efe6d6] bg-[#faf6ee] px-3 py-2",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
									className: "text-sm font-bold text-[#7f1d1d]",
									children: [
										"Page ",
										p.n,
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
											className: "ml-2 font-medium text-[#5c5348]",
											children: p.label
										})
									]
								})
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
								href: p.src,
								target: "_blank",
								rel: "noreferrer",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
									src: p.src,
									alt: `Exam page ${p.n}`,
									className: "block w-full bg-[#ddd2c0]"
								})
							})]
						}, p.n))
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
					className: "mt-8 mb-10 rounded-2xl border border-[#e0d4c0] bg-[#fffdf8] p-5 text-sm leading-relaxed text-[#3f3a34] sm:p-6",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
						className: "text-lg font-bold text-[#7f1d1d]",
						style: { fontFamily: "\"Source Serif 4\", Georgia, serif" },
						children: "Paper e ja ache"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("ul", {
						className: "mt-3 grid gap-1.5 sm:grid-cols-2",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: "Page 1 — Passage (Liberation War Museum) + Q.1 MCQ/True-False + Q.2–3" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: "Page 2 — Roni’s garden Q.4–5, rearrange Q.6, grammar Q.7, verbs Q.8" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: "Q.9 Paragraph — Necessity of Eating Healthy Food (Unit 12)" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: "Q.10 Letter — Asif to Belal, annual sports day" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", { children: "Full marks 70 · Time 2 hours 30 minutes · A4 × 2 pages" })
						]
					})]
				})
			]
		})]
	});
}
function DownloadCard({ href, icon, title, sub, cta, primary }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("a", {
		href,
		download: true,
		className: "group flex flex-col rounded-2xl border p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md " + (primary ? "border-[#7f1d1d] bg-[#7f1d1d] text-[#faf6ee]" : "border-[#e0d4c0] bg-white text-[#1c1917]"),
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mb-3 inline-flex size-9 items-center justify-center rounded-full " + (primary ? "bg-[#c9a227] text-[#4c1010]" : "bg-[#faf6ee] text-[#7f1d1d]"),
				children: icon
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", {
				className: "text-[15px] font-bold leading-snug",
				children: title
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "mt-1 flex-1 text-xs leading-relaxed " + (primary ? "text-[#f0d7b0]" : "text-[#5c5348]"),
				children: sub
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
				className: "mt-3 inline-flex items-center gap-1.5 text-sm font-semibold " + (primary ? "text-[#e8c547]" : "text-[#7f1d1d]"),
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Download, { className: "size-4" }), cta]
			})
		]
	});
}
function Step({ n, title, children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
		className: "rounded-xl bg-[#faf6ee] p-3",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
				className: "text-[11px] font-bold tracking-wider text-[#c9a227] uppercase",
				children: ["Step ", n]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "mt-0.5 font-bold text-[#7f1d1d]",
				children: title
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "mt-1 text-[13px]",
				children
			})
		]
	});
}
//#endregion
export { Home as component };
