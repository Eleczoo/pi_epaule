#import "conf.typ": *
#import "@preview/oxifmt:0.2.0": strfmt
#import "@preview/codly:0.2.0": * // CODE



#let today = datetime.today()
#show: codly-init.with() // Setup for code blocks

#show: doc => conf(
	title: [Title of the document],
	subtitle: [Subtitle of the document],
	date: today.display("[day]/[month]/[year]"),
	logo: "images/graham.jpg",
	authors: (
    	(
		),
	),
	doc,
)

// ! SETUP CODES BLOCKS
#let icon(codepoint) = {
	v(-1em)
	box(height: 0.8em, baseline: -1em,)
	//h(0.5em)
} 
#codly(languages: (
	rust: (name: "Rust", icon : icon(""), color: rgb("#CE412B")),
	python: (name: "Python", icon : icon(""), color: rgb("#3572A5")),
	c: (name: "C", icon : icon(""), color: rgb("#555555")),
	bash: (name: "Bash", icon : icon(""), color: rgb("#89E234")),
),
	stroke-color: luma(200),
	stroke-width: 1pt,
	zebra-color: luma(240),
)
// ! ----------