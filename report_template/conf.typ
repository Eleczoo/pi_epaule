#import "@preview/codly:0.2.0": *


// The project function defines how your document looks.
// It takes your content and some metadata and formats it.
// Go ahead and customize it to your liking!
#let conf(
	title: "",
	subtitle: "",
	abstract: [],
	authors: (),
	date: "",
	logo: "",
	body,
) = {
	set page(numbering: "1", number-align: center)

	// ? Latex look
	set page(margin: 2.5cm) 				// ! GLOBAL MARGIN 
	set par(leading: 1.5mm, justify: true)  // ! INTERLINE
	set text(font: "New Computer Modern")	 
	show raw: set text(font: "New Computer Modern Mono")
	set par(spacing: 1cm)
	show heading: set block(above: 1.2em, below: 1.2em)


	// ! FONTS
	// let body-font = "Linux Libertine"
	let body-font = "New Computer Modern"
	//let sans-font = "Linux Libertine Mono"
	let sans-font = "New Computer Modern Mono"

	// ! TEXT AND HEADING STYLE  
	set text(font: body-font, lang: "en", size: 12pt, weight: 400)
	show heading: set text(font: sans-font)
	//set heading(numbering: "1.1.1.", )

	// ! EQUATIONS
	set math.equation(numbering: "(1)")
	show math.equation: set text(12pt) // BIGGER EQUATIONS

	// ! LIST STYLING
	set list(tight : false, marker: ([■], [□]), indent: 0cm, spacing: 0.4cm)
	set enum(spacing: 0.4cm, indent: 0cm)
	//show list: set block(spacing: 2cm, above: 0.5cm, below: 0.5cm)
	//show enum: set block(spacing: 5cm, above: 0.5cm, below: 0.5cm)

	// ! MAIN BODY
	set par(justify: true)
	body
}

// ! CODE
// OLD Source : https://github.com/typst/typst/issues/344
// NEW Source : https://github.com/Dherse/codly/tree/main
// #import "@preview/codly:0.2.0": *

// Commands, without line numbers.
#let cmd(body) = {
		codly(enable-numbers: false)
		body
		codly(enable-numbers: true)
}