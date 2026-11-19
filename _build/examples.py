# Example gallery entries for examples.html.
# "inputs": (glob relative to the example root, published file name).
# Entries with from_code=True are read from the SoftDFT code folder instead.

CATEGORIES = {
    "exact": "Exact & consistency checks",
    "hs": "Hard spheres",
    "polymer": "Polymers & brushes",
    "elec": "Electrolytes",
    "reg": "Charge regulation",
    "lit": "Literature benchmarks",
}

# System sketches (assets/img/sketches/sketchNN.png), keyed by example slug.
SKETCHES = {
    "ideal-gas-slit": 1, "patterned-3d-ideal-gas": 2, "binary-hs-pressure": 3, "bulk-derivatives": 4,
    "hs-wall": 5, "hs-density-sweep": 6, "cross-dimension-slit": 7, "neutral-brush": 8,
    "segment-conservation": 9, "charged-slit": 10, "charge-reversal": 11, "asymmetric-electrolyte": 12,
    "two-step-acid": 13, "charge-regulating-brush": 14, "weak-brush-sweep": 15,
    "weak-brush-published": 16, "square-well-adsorption": 17, "primitive-electrolyte-edl": 22,
}

EXAMPLES = [
    # ------------------------------------------------------------ exact checks
    dict(slug="ideal-gas-slit", cat="exact", tags=["1D", "ideal"],
         title="Ideal gas in a hard-wall slit",
         inputs=[("1_example_*/data/input.yaml", "input.yaml")],
         summary="<p>The simplest possible inhomogeneous calculation: an ideal gas between two hard walls. "
                 "With only the ideal free-energy term, the equilibrium density is the Boltzmann profile, "
                 "so SoftDFT can be compared with the exact answer at every grid point.</p>",
         results=["Maximum absolute profile error about 7&times;10<sup>&minus;18</sup> (machine precision)."],
         fig="ex01_ideal_gas.png", alt="SoftDFT and exact ideal-gas density profiles overlap",
         caption="SoftDFT (dashed) lies on top of the exact Boltzmann profile (grey)."),
    dict(slug="patterned-3d-ideal-gas", cat="exact", tags=["3D", "external field"],
         title="Three-dimensional ideal gas in a patterned external field",
         inputs=[("2_example_*/data/input.yaml", "input.yaml")],
         summary="<p>A user-supplied external potential that varies along <em>x</em>, <em>y</em> and <em>z</em> "
                 "(including a mixed <em>x+y+z</em> term) is read from file on a 9&times;9&times;9 grid. "
                 "The ideal-gas density must equal &rho;<sub>b</sub>&nbsp;exp[&minus;&beta;V(x,y,z)] in every cell, "
                 "which tests the 3D grid indexing and the <code>input_external</code> field reader.</p>",
         results=["Bulk density &rho;<sub>b</sub>d<sup>3</sup> = 0.1; the local density ranges from 0.039 to 0.258 "
                  "across the box and varies along all three axes.",
                  "Potential mapping error: 0.", "Maximum density error against the exact formula: 8.3&times;10<sup>&minus;17</sup>."]),
    dict(slug="binary-hs-pressure", cat="exact", tags=["bulk", "mFMT"],
         title="Binary hard-sphere mixture: bulk pressure",
         inputs=[("3_example_*/data/input.yaml", "input.yaml")],
         summary="<p>A bulk (iLST) calculation for a two-component hard-sphere mixture. The compressibility "
                 "factor from SoftDFT's excluded-volume model is compared with the analytical "
                 "Boyle&ndash;Mansoori&ndash;Carnahan&ndash;Starling&ndash;Leland (BMCSL) equation of state.</p>",
         results=["State point: &rho;<sub>A</sub>d<sup>3</sup> = 0.08 (d<sub>A</sub> = 1.0), &rho;<sub>B</sub>d<sup>3</sup> = 0.06 "
                  "(d<sub>B</sub> = 1.5), packing fraction 0.148.",
                  "SoftDFT <em>Z</em> = 1.8281429558181252; BMCSL <em>Z</em> = 1.8281429558181255.",
                  "Relative error 1.2&times;10<sup>&minus;16</sup> (machine precision)."]),
    dict(slug="bulk-derivatives", cat="exact", tags=["bulk", "square well"],
         title="Bulk thermodynamic consistency",
         inputs=[("4_example_*/data/input.yaml", "input.yaml")],
         summary="<p>A neutral A/B mixture with different diameters and ideal, mFMT and square-well terms. "
                 "Each density is perturbed by &plusmn;10<sup>&minus;6</sup>; the central-difference derivative "
                 "of the excess free energy is compared with SoftDFT's excess chemical potential, and the "
                 "pressure identity <em>P</em> = &Sigma;&rho;<sub>i</sub> &minus; <em>f</em><sub>ex</sub> + "
                 "&Sigma;&rho;<sub>i</sub>&mu;<sub>ex,i</sub> is checked.</p>",
         results=["Maximum derivative discrepancy 7.2&times;10<sup>&minus;12</sup>.",
                  "Bulk pressure &beta;<em>P</em>d<sup>3</sup> = 0.103623 from SoftDFT and from the identity; "
                  "discrepancy 0."]),
    dict(slug="two-step-acid", cat="exact", tags=["bulk", "reactions", "pH"],
         title="Two-step acid equilibrium",
         inputs=[("13_example_*/data/ph7/input.yaml", "input.yaml")],
         summary="<p>A species with three charge states (A, B<sup>&minus;</sup>, C<sup>2&minus;</sup>) undergoes "
                 "A &#8652; B + H<sup>+</sup> (p<em>K</em> 4) and B &#8652; C + H<sup>+</sup> (p<em>K</em> 8). "
                 "At pH 4, 7 and 10 the state fractions are compared with elementary mass action, "
                 "A:B:C = 1 : 10<sup>pH&minus;4</sup> : 10<sup>2pH&minus;12</sup>. "
                 "The published input is the pH 7 case.</p>",
         results=["Largest fraction error 2.3&times;10<sup>&minus;16</sup>; net charge zero to machine precision."],
         fig="ex13_two_step_acid.png", alt="Bar chart of state fractions at pH 4, 7, 10 with mass-action points",
         caption="Bars: SoftDFT state fractions. Dots: ideal mass action."),

    # ------------------------------------------------------------ hard spheres
    dict(slug="hs-wall", cat="hs", tags=["1D", "mFMT"],
         title="Hard spheres at a planar hard wall",
         inputs=[("5_example_*/data/input.yaml", "input.yaml")],
         summary="<p>A one-component hard-sphere fluid at &rho;<sub>b</sub>d<sup>3</sup> = 0.305 next to a hard wall. "
                 "The contact value theorem requires the contact density to equal &beta;<em>P</em> of the bulk fluid.</p>",
         results=["Converged in 17 iterations.",
                  "Contact density 0.60579 vs. &beta;<em>P</em> = 0.60714 (0.22% at grid spacing 0.1d)."],
         fig="ex05_hs_wall.png", alt="Oscillating hard-sphere density profile near a wall",
         caption="Layering of hard spheres near the wall, normalized by bulk density."),
    dict(slug="hs-density-sweep", cat="hs", tags=["1D", "mFMT", "MD comparison"],
         title="Hard-sphere wall: density sweep and comparison with MD",
         inputs=[("6_example_*/data/rho_0p305__h_0p025/input.yaml", "input.yaml")],
         summary="<p>Bulk densities 0.305, 0.701 and 0.857 are each solved on four grids (0.2d to 0.025d). "
                 "The contact error shrinks roughly quadratically with grid spacing. Profiles at the exact state "
                 "points of Davidchack, Laird &amp; Roth are then compared with their published molecular-dynamics "
                 "density profiles.</p>",
         results=["Profile RMSE vs. MD over 0.5&ndash;5d: 0.05% (&rho;=0.305), 1.8% (0.701) and 8.6% (0.857) of bulk density.",
                  "The high-density difference persists under grid refinement and reflects the functional, "
                  "consistent with the trend reported in the reference."],
         fig="ex06_md_overlay.png", alt="SoftDFT and MD hard-sphere profiles at three densities",
         caption="SoftDFT profiles overlaid on the published MD data.",
         ref="Reference: R. L. Davidchack, B. B. Laird, R. Roth, <em>Condens. Matter Phys.</em> 19, 23001 (2016); "
             "MD data from the University of Leicester Figshare record."),
    dict(slug="cross-dimension-slit", cat="hs", tags=["1D", "2D", "3D"],
         title="Same slit in 1D, 2D and 3D",
         inputs=[("7_example_*/data/1d/input.yaml", "input_1d.yaml"),
                 ("7_example_*/data/2d/input.yaml", "input_2d.yaml"),
                 ("7_example_*/data/3d/input.yaml", "input_3d.yaml")],
         summary="<p>A hard-sphere fluid (&rho;<sub>b</sub>d<sup>3</sup> = 0.2) between walls 6d apart is solved "
                 "as a 1D problem and again with one or two periodic lateral directions. Averaged over the lateral "
                 "directions, the 2D and 3D profiles must match the 1D result.</p>",
         results=["All residuals below 1.8&times;10<sup>&minus;8</sup>.",
                  "2D and 3D profiles differ from 1D by less than 4&times;10<sup>&minus;16</sup>."],
         fig="ex07_cross_dimension.png", alt="1D, 2D and 3D hard-sphere slit profiles overlap",
         caption="1D, 2D and 3D calculations give the same profile."),

    # ------------------------------------------------------------ polymers
    dict(slug="neutral-brush", cat="polymer", tags=["1D", "TPT1", "grafted"],
         title="Neutral grafted polymer brush",
         inputs=[("8_example_*/data/input.yaml", "input.yaml")],
         summary="<p>Five-bead chains grafted to the left wall (0.05 chains per d<sup>2</sup>) in a 15d slit with a "
                 "dilute solvent, using ideal and TPT1-mFMT chain terms. A compact teaching example for the "
                 "<code>fixed</code> species block.</p>",
         results=["Residual 6.8&times;10<sup>&minus;8</sup>; brush height 2.43d (<code>brush_height.txt</code>)."],
         fig="ex08_neutral_brush.png", alt="Polymer bead and solvent density profiles in a brush",
         caption="Polymer-bead and solvent density profiles."),
    dict(slug="segment-conservation", cat="polymer", tags=["1D", "grid convergence"],
         title="Polymer segment conservation and grid refinement",
         inputs=[("9_example_*/data/n5_h005/input.yaml", "input.yaml")],
         summary="<p>Grafted chains of 2, 5 and 10 beads (0.02 chains per d<sup>2</sup>). Every segment's integrated "
                 "amount should equal the grafting density. The five-bead chain is solved at grid spacings 0.2, 0.1 "
                 "and 0.05 to show how the discretization error falls with refinement.</p>",
         results=["Five-bead chain, maximum segment-amount error: 5.8% (0.2d), 2.8% (0.1d), 1.4% (0.05d).",
                  "Use a fine grid when quantitative segment profiles matter."],
         fig="ex09_segment_conservation.png", alt="Segment-amount error by segment for three grid spacings",
         caption="Five-bead chain: the error in each segment's amount halves each time the grid spacing is halved."),
    dict(slug="charge-regulating-brush", cat="polymer", tags=["1D", "Ising DFT", "pH"],
         title="Charge-regulating weak polyacid brush",
         inputs=[("14_example_*/data/input.yaml", "input.yaml")],
         summary="<p>Eight-bead weak-acid chains (A &#8652; B<sup>&minus;</sup> + H<sup>+</sup>, p<em>K</em> 4.756) "
                 "grafted at 0.05 chains per d<sup>2</sup>, at pH 7 with monovalent salt. Ising DFT solves the "
                 "segment ionization together with the chain conformations, ion distributions and electrostatic "
                 "potential.</p>",
         results=["Residual 9.4&times;10<sup>&minus;8</sup>; mean ionized fraction 0.91.",
                  "Needed smaller mixing (<code>damping</code> = <code>mixing_max</code> = 0.05)."],
         fig="ex14_regulating_brush.png", alt="Neutral and ionized segment and ion profiles in a weak polyacid brush",
         caption="Neutral (A) and ionized (B) segments, counterions and coions."),
    dict(slug="weak-brush-sweep", cat="polymer", tags=["1D", "Ising DFT", "parameter sweep"],
         title="Weak polyacid brush: pH and salt sweep",
         inputs=[("15_example_*/data/ph7_salt001/input.yaml", "input.yaml")],
         summary="<p>The brush above at pH 5 and 7 and two salt concentrations. Ionization rises with pH and with "
                 "salt (salt screens the electrostatic penalty for charging); the brush swells with pH and "
                 "shrinks with added salt.</p>",
         results=["pH 7, salt 0.01: ionized fraction 0.911, height 4.60d.",
                  "pH 7, salt 0.05: ionized fraction 0.974, height 4.26d."],
         fig="ex15_ph_salt_sweep.png", alt="Mean ionized fraction vs pH for two salt concentrations",
         caption="Mean ionized fraction at two salt concentrations."),

    # ------------------------------------------------------------ electrolytes
    dict(slug="charged-slit", cat="elec", tags=["1D", "MSA", "Poisson"],
         title="1:1 electrolyte between oppositely charged walls",
         inputs=[("10_example_*/data/input.yaml", "input.yaml")],
         summary="<p>Equal-size monovalent ions (&rho;<sub>b</sub>d<sup>3</sup> = 0.02 each) in a 12d slit with wall "
                 "charges &minus;0.01 and +0.01 e/d<sup>2</sup>, using ideal, mFMT and MSA terms plus the FFT "
                 "Poisson solver. Checks: residual, left/right antisymmetry, neutrality and counterion enrichment.</p>",
         results=["Residual 4.9&times;10<sup>&minus;8</sup>; net mobile charge 3&times;10<sup>&minus;15</sup>.",
                  "Counterion/coion ratio at contact: 1.52."],
         fig="ex10_charged_slit.png", alt="Cation and anion density and potential profiles in a charged slit",
         caption="Ion densities (left axis) and reduced potential (right axis)."),
    dict(slug="charge-reversal", cat="elec", tags=["1D", "symmetry"],
         title="Charge-reversal symmetry",
         inputs=[("11_example_*/data/negative/input.yaml", "input_negative.yaml"),
                 ("11_example_*/data/positive/input.yaml", "input_positive.yaml")],
         summary="<p>Two equally charged walls (&minus;0.005 e/d<sup>2</sup>) and the same system with both charges "
                 "reversed. Cation and anion profiles must swap exactly and the potential must change sign; "
                 "fluid plus wall charge must be neutral.</p>",
         results=["Profile-reversal error 1.9&times;10<sup>&minus;13</sup>; potential-reversal error 3.6&times;10<sup>&minus;12</sup>.",
                  "Charge-balance error 4.3&times;10<sup>&minus;9</sup> (with trapezoidal weights)."],
         fig="ex11_charge_reversal.png", alt="Cation and anion profiles swap when wall charges reverse",
         caption="Solid: negative walls. Dashed: reversed walls. The curves coincide pairwise."),
    dict(slug="asymmetric-electrolyte", cat="elec", tags=["1D", "2:1", "size asymmetry"],
         title="Size- and valence-asymmetric 2:1 electrolyte",
         inputs=[("12_example_*/data/charged/input.yaml", "input.yaml")],
         summary="<p>Divalent cations (diameter 1.2d) and monovalent anions (0.8d) in a 16d slit with walls at "
                 "&minus;0.02 and +0.02 e/d<sup>2</sup>, compared with an uncharged-wall control.</p>",
         results=["First accessible cation bin at the negative wall: 1.78&times; bulk; anion at the positive wall: 1.26&times; bulk."],
         fig="ex12_asymmetric_electrolyte.png", alt="Density profiles of divalent cations and monovalent anions",
         caption="Charged walls (solid) vs. neutral control (dotted)."),
    dict(slug="square-well-adsorption", cat="elec", tags=["1D", "square well", "selective"],
         title="Selective adsorption with square-well attraction",
         inputs=[("17_example_*/data/attractive/input.yaml", "input.yaml")],
         summary="<p>Two neutral species share a slit; only A feels a square-well attraction to the wall, while both "
                 "keep A&ndash;A and A&ndash;B square-well pair interactions. Shows the <code>sw_walls</code> field "
                 "and the <code>pairs</code> block.</p>",
         results=["Contact density of A is 7.2&times; its value in the non-attractive control."],
         fig="ex17_square_well.png", alt="Density of species A and B with and without wall attraction",
         caption="Attractive wall (solid) vs. control (dotted)."),

    # ------------------------------------------------------------ charge regulation
    dict(slug="charge-regulated-slit", cat="reg", tags=["1D", "FFT Poisson", "pH"], from_code=True,
         title="Charge-regulated walls",
         inputs=[("charge_regulated_slit/input.yaml", "input.yaml")],
         summary="<p>Each wall carries ionizable sites (Γ = 0.02 e/d<sup>2</sup>): acid sites on the left and base "
                 "sites on the right, both with p<em>K</em><sub>a</sub> 7. The site charge follows "
                 "log[&alpha;/(1&minus;&alpha;)] = ln10&middot;(pH &minus; p<em>K</em><sub>a</sub>) + &beta;e&psi;<sub>wall</sub> "
                 "(sign reversed for bases) and is solved self-consistently with the ion densities and the FFT "
                 "Poisson solution. The reservoir pH is taken from the proton species <code>Y</code>.</p>",
         results=["Wall charges move from &plusmn;0.0100 (zero-potential guess) to &plusmn;0.00879 e/d<sup>2</sup>.",
                  "Charge-law residual 3&times;10<sup>&minus;10</sup>; full DFT residual 1.2&times;10<sup>&minus;7</sup>."],
         fig="excr_regulated_slit.png", alt="Cation, anion and potential profiles between an acid wall and a base wall",
         caption="Ion densities (left axis) and reduced potential (right axis). The protons, at about 10<sup>&minus;8</sup>, are too dilute to show."),
    dict(slug="mixed-fixed-regulated", cat="reg", tags=["1D", "mixed walls"], from_code=True,
         title="Fixed-charge wall facing a charge-regulated wall",
         inputs=[("mixed_fixed_regulated_slit/input.yaml", "input.yaml")],
         summary="<p><code>charged_walls</code> and <code>charge_regulated_walls</code> can be combined; their "
                 "charges add on each wall. Here the left wall has a fixed charge of &minus;0.01 and the right wall "
                 "has regulated base sites.</p>",
         results=["Fixed wall stays at &minus;0.010; the regulated wall converges to +0.00879 e/d<sup>2</sup>.",
                  "Charge-law residual 1.7&times;10<sup>&minus;10</sup>; full DFT residual 7.8&times;10<sup>&minus;7</sup>.",
                  "&minus;0.010 is what the acid wall of the previous example would carry with no regulation "
                  "(half its sites charged at pH = p<em>K</em><sub>a</sub>). Comparing the two left walls isolates the "
                  "regulation effect: the wall potential weakens from &minus;0.274 to &minus;0.244 and the counterion "
                  "contact density drops from 0.0248 to 0.0242."],
         fig="excr_mixed_walls.png", alt="Ion densities and potential near a fixed-charge wall compared with a charge-regulated acid wall",
         caption="Near the left wall: fixed charge (solid) vs. regulated acid sites (dashed). The negative potential "
                 "holds protons at the surface, suppresses dissociation and weakens the double layer."),

    # ------------------------------------------------------------ literature
    dict(slug="primitive-electrolyte-edl", cat="lit", tags=["1D", "MC comparison", "physical units"],
         title="Electric double layer: comparison with Monte Carlo",
         inputs=[("22_example_*/data/input.yaml", "input.yaml")],
         summary="<p>A 0.1 M 1:1 primitive-model electrolyte (3 &Aring; ions) between electrodes at "
                 "&mp;0.02 C/m<sup>2</sup>, set up in physical units with <code>reduced_units.l_sc: 0.3</code> nm. "
                 "SoftDFT (mFMT + MSA) is compared directly with the published raw Monte Carlo profiles.</p>",
         results=["Cation RMSE 0.0028 M and anion RMSE 0.0014 M over 1.6&ndash;30 &Aring;.",
                  "Wall potential relative to midplane: &minus;1.189 kT/e (SoftDFT) vs. &minus;1.202 kT/e (MC)."],
         fig="ex22_mc_overlay.png", alt="SoftDFT ion and potential profiles overlaid on Monte Carlo data",
         caption="Lines: SoftDFT. Points: Monte Carlo.",
         ref="Reference: M. Valiskó, T. Kristóf, D. Gillespie, D. Boda, <em>J. Chem. Phys.</em> 148, 024701 (2018), "
             "doi:10.1063/1.5022036."),
    dict(slug="weak-brush-published", cat="lit", tags=["1D", "Ising DFT", "physical units"],
         title="Weak polyacid brush at published conditions",
         inputs=[("16_example_*/data/input.yaml", "input.yaml")],
         summary="<p>25-segment weak-acid chains (bead diameter 0.355 nm, p<em>K</em> 4.0) grafted at 0.79 chains/nm<sup>2</sup> "
                 "in 5 mM NaCl, matching the conditions of Gallegos <em>et&nbsp;al.</em> (2026). The input shows how "
                 "physical concentrations and grafting densities are converted to reduced units.</p>",
         results=["pH 2.0 profiles converge with grid refinement beyond ~0.8 nm.",
                  "pH 6.0 mean ionization 0.230&ndash;0.233, within the range read from the published curve (about 0.21&ndash;0.24)."],
         fig="ex16_grid_profiles.png", alt="Segment concentration profiles of a weak polyacid brush at three grid spacings",
         caption="Segment concentration vs. distance at pH 2.0 on three grids.",
         ref="Reference: A. Gallegos, R. Lunkad, M. Müller, J. Wu, <em>J. Phys. Chem. B</em> 130, 4041 (2026), "
             "doi:10.1021/acs.jpcb.6c00544."),
]
