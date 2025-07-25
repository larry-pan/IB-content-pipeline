import cohere
from dotenv import dotenv_values
from cohere.finetuning import Settings, FinetunedModel, BaseModel
import json

MODEL_NAME = "test-finetune-model"
config = dotenv_values(".env")
co = cohere.ClientV2(config.get("COHERE_KEY"))

system_prompt = (
    "You are an assistant that generates IB-style advanced high school and early university math questions and markschemes. "
    "All mathematical expressions MUST be written in valid LaTeX format. "
    "You will generate a JSON list called 'parts', where each element is a sub-question. Each sub-question "
    "must have:\n\n"
    "  - 'content': a clear and challenging question string with equations and numbers in latex.\n"
    "  - 'marks': how many marks the question is worth, with more marks for harder questions.\n"
    "  - 'markscheme': an IB-style markscheme string which focuses as much as possible on concise numerical steps with "
    "almost no word descriptions, showing the major computational steps in latex to solve the problem "
    "while including exactly how mark are awarded. \n"
    "  - 'subtopics' for a list of IB subtopics that the question covers, which may overlap into other topics.\n\n"
    "Make sure all questions and answers are rigorous and well-aligned with the IB Math syllabus.\n\n"
    "Topics and subtopics are and strictly limited to:\n\n"
    "- Number and Algebra: standard form, arithmetic sequences and series, geometric sequences and series, "
    "financial applications, logarithms, simple proof, laws of exponents and logs, sum of infinite geometric sequence, "
    "binomial theorem, permutations and combinations, partial fractions, complex numbers, polar and Euler form, "
    "complex roots of polynomials, proof by induction, systems of linear equations\n"
    "- Functions: equations of straight lines, function notation domain and range, graphing, key features of graphs, "
    "composite functions, quadratic functions, solutions of quadratic equations, reciprocal and rational functions, "
    "exponential and logarithmic functions, solving equations, transformation of functions, factor and remainder theorems, "
    "odd and even functions, solutions of inequalities, graphing modulus equations\n"
    "- Geometry and Trigonometry: 3D space and volume, 2D and 3D trigonometry, applications of trigonometry, "
    "circles and radians, unit circle definitions, Pythagorean identity, circular functions, solving trigonometric equations, "
    "reciprocal trigonometric ratios, compound angle identities, vector definitions, scalar product, vector equations, "
    "classification of lines, vector product, intersections of lines and planes\n"
    "- Statistics and Probability: sampling techniques, histograms and data visualization, measures of central tendency, "
    "correlation and regression, probability concepts, combined and conditional probability, discrete random variables, "
    "binomial distribution, normal distribution, regression analysis, independence testing, Bayes theorem, "
    "properties of random variables\n"
    "- Calculus: differential calculus introduction, increasing and decreasing functions, differentiating polynomials, "
    "tangents and normals, integration introduction, chain product and quotient rules, second derivative, optimization, "
    "kinematics, indefinite integration, definite integrals, limits and L'Hopital's rule, implicit functions, "
    "integration techniques, areas and volumes, differential equations, Maclaurin series\n"
)

training_data = {
    "messages": [
        {"role": "System", "content": system_prompt},
        # Standard Form
        {
            "role": "User",
            "content": "Express $\\frac{2.4 \\times 10^{-3} \\times 8.1 \\times 10^{6}}{3.6 \\times 10^{2}}$ in standard form.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Express $\\frac{2.4 \\times 10^{-3} \\times 8.1 \\times 10^{6}}{3.6 \\times 10^{2}}$ in standard form.",
                "marks": 3,
                "markscheme": "$\\frac{2.4 \\times 8.1}{3.6} \\times \\frac{10^{-3} \\times 10^{6}}{10^{2}}$ (M1)\n$5.4 \\times 10^{1}$ (A1)\n$5.4 \\times 10^{1}$ or $54$ (A1) [3 marks]",
                "subtopics": ["Standard form"],
                "topic": "Number and algebra",
            },
        },
        # Arithmetic Sequences
        {
            "role": "User",
            "content": "The sum of the first $n$ terms of an arithmetic sequence is $S_n = 3n^2 + 2n$. Find the 15th term of the sequence.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "The sum of the first $n$ terms of an arithmetic sequence is $S_n = 3n^2 + 2n$. Find the 15th term of the sequence.",
                "marks": 4,
                "markscheme": "$a_{15} = S_{15} - S_{14}$ (M1)\n$S_{15} = 3(15)^2 + 2(15) = 705$ (A1)\n$S_{14} = 3(14)^2 + 2(14) = 616$ (A1)\n$a_{15} = 705 - 616 = 89$ (A1) [4 marks]",
                "subtopics": ["Arithmetic sequences and series"],
                "topic": "Number and algebra",
            },
        },
        # Geometric Sequences
        {
            "role": "User",
            "content": "A geometric series has first term $a = 8$ and common ratio $r = -\\frac{1}{2}$. Find the sum of the first 10 terms.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "A geometric series has first term $a = 8$ and common ratio $r = -\\frac{1}{2}$. Find the sum of the first 10 terms.",
                "marks": 3,
                "markscheme": "$S_n = a\\frac{1-r^n}{1-r}$ (M1)\n$S_{10} = 8\\frac{1-(-\\frac{1}{2})^{10}}{1-(-\\frac{1}{2})} = 8\\frac{1-\\frac{1}{1024}}{\\frac{3}{2}}$ (A1)\n$S_{10} = \\frac{341}{64}$ (A1) [3 marks]",
                "subtopics": ["Geometric sequences and series"],
                "topic": "Number and algebra",
            },
        },
        # Financial Applications
        {
            "role": "User",
            "content": "Sarah invests $5000 at 4.5% per annum compound interest. After how many complete years will her investment first exceed $8000?",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Sarah invests $5000 at 4.5% per annum compound interest. After how many complete years will her investment first exceed $8000?",
                "marks": 4,
                "markscheme": "$5000(1.045)^n > 8000$ (M1)\n$(1.045)^n > 1.6$ (A1)\n$n > \\frac{\\log(1.6)}{\\log(1.045)} = 10.57...$ (A1)\n$n = 11$ years (A1) [4 marks]",
                "subtopics": ["Financial applications"],
                "topic": "Number and algebra",
            },
        },
        # Logarithms
        {"role": "User", "content": "Solve $2\\log_3(x-1) - \\log_3(x+5) = 1$ for $x$."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Solve $2\\log_3(x-1) - \\log_3(x+5) = 1$ for $x$.",
                "marks": 5,
                "markscheme": "$\\log_3(x-1)^2 - \\log_3(x+5) = 1$ (M1)\n$\\log_3\\frac{(x-1)^2}{x+5} = 1$ (A1)\n$\\frac{(x-1)^2}{x+5} = 3$ (A1)\n$(x-1)^2 = 3(x+5)$, $x^2-5x-14=0$ (A1)\n$x = 7$ (A1) [5 marks]",
                "subtopics": ["Logarithms"],
                "topic": "Number and algebra",
            },
        },
        # Laws of Exponents
        {
            "role": "User",
            "content": "Simplify $\\frac{3^{2x+1} \\cdot 9^{x-2}}{27^{x-1}}$ and express your answer in the form $3^k$ where $k$ is in terms of $x$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Simplify $\\frac{3^{2x+1} \\cdot 9^{x-2}}{27^{x-1}}$ and express your answer in the form $3^k$ where $k$ is in terms of $x$.",
                "marks": 4,
                "markscheme": "$\\frac{3^{2x+1} \\cdot (3^2)^{x-2}}{(3^3)^{x-1}}$ (M1)\n$\\frac{3^{2x+1} \\cdot 3^{2x-4}}{3^{3x-3}}$ (A1)\n$3^{(2x+1)+(2x-4)-(3x-3)}$ (A1)\n$3^{x}$ (A1) [4 marks]",
                "subtopics": ["Laws of exponents and logs"],
                "topic": "Number and algebra",
            },
        },
        # Infinite Geometric Series
        {"role": "User", "content": "Find the exact value of $\\sum_{n=1}^{\\infty} \\frac{2}{3^n}$."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Find the exact value of $\\sum_{n=1}^{\\infty} \\frac{2}{3^n}$.",
                "marks": 3,
                "markscheme": "$a = \\frac{2}{3}$, $r = \\frac{1}{3}$ (M1)\n$S_{\\infty} = \\frac{a}{1-r} = \\frac{\\frac{2}{3}}{1-\\frac{1}{3}}$ (A1)\n$S_{\\infty} = 1$ (A1) [3 marks]",
                "subtopics": ["Sum of infinite geometric sequence"],
                "topic": "Number and algebra",
            },
        },
        # Binomial Theorem
        {
            "role": "User",
            "content": "Find the coefficient of $x^4$ in the expansion of $(2x - \\frac{1}{x})^{10}$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Find the coefficient of $x^4$ in the expansion of $(2x - \\frac{1}{x})^{10}$.",
                "marks": 4,
                "markscheme": "General term: $\\binom{10}{r}(2x)^{10-r}(-\\frac{1}{x})^r$ (M1)\n$\\binom{10}{r}2^{10-r}(-1)^r x^{10-r-r} = \\binom{10}{r}2^{10-r}(-1)^r x^{10-2r}$ (A1)\n$10-2r = 4$, so $r = 3$ (A1)\n$\\binom{10}{3}2^7(-1)^3 = -15360$ (A1) [4 marks]",
                "subtopics": ["Binomial theorem"],
                "topic": "Number and algebra",
            },
        },
        # Permutations and Combinations
        {
            "role": "User",
            "content": "In how many ways can 8 people be arranged in a row if 3 specific people must sit together?",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "In how many ways can 8 people be arranged in a row if 3 specific people must sit together?",
                "marks": 3,
                "markscheme": "Treat 3 people as one unit: 6 units to arrange (M1)\n$6! \\times 3!$ arrangements (A1)\n$43200$ (A1) [3 marks]",
                "subtopics": ["Permutations and combinations"],
                "topic": "Number and algebra",
            },
        },
        # Partial Fractions
        {"role": "User", "content": "Express $\\frac{5x+7}{(x+1)(x+3)}$ in partial fractions."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Express $\\frac{5x+7}{(x+1)(x+3)}$ in partial fractions.",
                "marks": 4,
                "markscheme": "$\\frac{5x+7}{(x+1)(x+3)} = \\frac{A}{x+1} + \\frac{B}{x+3}$ (M1)\n$5x+7 = A(x+3) + B(x+1)$ (A1)\n$x=-1: 2 = 2A$, so $A=1$; $x=-3: -8 = -2B$, so $B=4$ (A1)\n$\\frac{1}{x+1} + \\frac{4}{x+3}$ (A1) [4 marks]",
                "subtopics": ["Partial fractions"],
                "topic": "Number and algebra",
            },
        },
        # Complex Numbers
        {"role": "User", "content": "If $z = 3 + 4i$, find $z^2$ and express in the form $a + bi$."},
        {
            "role": "Chatbot",
            "content": {
                "content": "If $z = 3 + 4i$, find $z^2$ and express in the form $a + bi$.",
                "marks": 3,
                "markscheme": "$z^2 = (3+4i)^2$ (M1)\n$= 9 + 24i + 16i^2$ (A1)\n$= -7 + 24i$ (A1) [3 marks]",
                "subtopics": ["Complex numbers"],
                "topic": "Number and algebra",
            },
        },
        # Polar Form
        {"role": "User", "content": "Express $z = -1 + i\\sqrt{3}$ in polar form."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Express $z = -1 + i\\sqrt{3}$ in polar form.",
                "marks": 4,
                "markscheme": "$r = \\sqrt{(-1)^2 + (\\sqrt{3})^2} = 2$ (A1)\n$\\tan\\theta = \\frac{\\sqrt{3}}{-1} = -\\sqrt{3}$ in second quadrant (M1)\n$\\theta = \\frac{2\\pi}{3}$ (A1)\n$z = 2e^{i\\frac{2\\pi}{3}}$ or $z = 2(\\cos\\frac{2\\pi}{3} + i\\sin\\frac{2\\pi}{3})$ (A1) [4 marks]",
                "subtopics": ["Polar and Euler form"],
                "topic": "Number and algebra",
            },
        },
        # Complex Roots of Polynomials
        {"role": "User", "content": "Find all roots of $z^4 + 4z^2 + 5 = 0$."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Find all roots of $z^4 + 4z^2 + 5 = 0$.",
                "marks": 5,
                "markscheme": "Let $w = z^2$: $w^2 + 4w + 5 = 0$ (M1)\n$w = \\frac{-4 \\pm \\sqrt{16-20}}{2} = \\frac{-4 \\pm 2i}{2} = -2 \\pm i$ (A1)\n$z^2 = -2 + i$ or $z^2 = -2 - i$ (A1)\n$|-2+i| = \\sqrt{5}$, $\\arg(-2+i) = \\pi - \\arctan(\\frac{1}{2})$ (M1)\n$z = \\pm\\sqrt[4]{5}e^{i(\\pi-\\arctan(\\frac{1}{2}))/2}$, $z = \\pm\\sqrt[4]{5}e^{i(\\pi+\\arctan(\\frac{1}{2}))/2}$ (A1) [5 marks]",
                "subtopics": ["Complex roots of polynomials"],
                "topic": "Number and algebra",
            },
        },
        # Proof by Induction
        {
            "role": "User",
            "content": "Prove by mathematical induction that $1^3 + 2^3 + 3^3 + ... + n^3 = \\frac{n^2(n+1)^2}{4}$ for all positive integers $n$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Prove by mathematical induction that $1^3 + 2^3 + 3^3 + ... + n^3 = \\frac{n^2(n+1)^2}{4}$ for all positive integers $n$.",
                "marks": 6,
                "markscheme": "Base case $n=1$: $1^3 = 1$ and $\\frac{1^2(2)^2}{4} = 1$  (A1)\nAssume true for $n=k$: $\\sum_{i=1}^k i^3 = \\frac{k^2(k+1)^2}{4}$ (M1)\nProve for $n=k+1$: $\\sum_{i=1}^{k+1} i^3 = \\frac{k^2(k+1)^2}{4} + (k+1)^3$ (M1)\n$= \\frac{k^2(k+1)^2 + 4(k+1)^3}{4} = \\frac{(k+1)^2[k^2 + 4(k+1)]}{4}$ (A1)\n$= \\frac{(k+1)^2(k^2+4k+4)}{4} = \\frac{(k+1)^2(k+2)^2}{4}$ (A1)\nTherefore true for all $n \\geq 1$ (A1) [6 marks]",
                "subtopics": ["Proof by induction"],
                "topic": "Number and algebra",
            },
        },
        # Systems of Linear Equations
        {
            "role": "User",
            "content": "Solve the system of equations: $2x + 3y - z = 7$, $x - 2y + 3z = 1$, $3x + y + 2z = 12$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Solve the system of equations: $2x + 3y - z = 7$, $x - 2y + 3z = 1$, $3x + y + 2z = 12$.",
                "marks": 6,
                "markscheme": "From equation 2: $x = 1 + 2y - 3z$ (M1)\nSubstitute into equation 1: $2(1 + 2y - 3z) + 3y - z = 7$ (A1)\n$7y - 7z = 5$ ... (4) (A1)\nSubstitute into equation 3: $3(1 + 2y - 3z) + y + 2z = 12$ (A1)\n$7y - 7z = 9$ ... (5) (A1)\nEquations (4) and (5) inconsistent: no solution (A1) [6 marks]",
                "subtopics": ["Systems of linear equations"],
                "topic": "Number and algebra",
            },
        },
    ]
}

eval_data = {
    "messages": [
        {"role": "System", "content": system_prompt},
        # Standard Form - Different approach: word problem with units
        {
            "role": "User",
            "content": "The mass of a hydrogen atom is approximately $1.67 \\times 10^{-27}$ kg. If Avogadro's number is $6.02 \\times 10^{23}$, find the mass of one mole of hydrogen atoms in standard form.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "The mass of a hydrogen atom is approximately $1.67 \\times 10^{-27}$ kg. If Avogadro's number is $6.02 \\times 10^{23}$, find the mass of one mole of hydrogen atoms in standard form.",
                "marks": 3,
                "markscheme": "Mass = $(1.67 \\times 10^{-27}) \\times (6.02 \\times 10^{23})$ (M1)\n$= 1.67 \\times 6.02 \\times 10^{-27+23}$ (A1)\n$= 1.01 \\times 10^{-3}$ kg (A1) [3 marks]",
                "subtopics": ["Standard form"],
                "topic": "Number and algebra",
            },
        },
        # Arithmetic Sequences - Different approach: finding first term and common difference
        {
            "role": "User",
            "content": "In an arithmetic sequence, the 5th term is 17 and the 12th term is 38. Find the first term and the sum of the first 20 terms.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "In an arithmetic sequence, the 5th term is 17 and the 12th term is 38. Find the first term and the sum of the first 20 terms.",
                "marks": 5,
                "markscheme": "$a_5 = a + 4d = 17$, $a_{12} = a + 11d = 38$ (M1)\n$7d = 21$, so $d = 3$ (A1)\n$a = 17 - 4(3) = 5$ (A1)\n$S_{20} = \\frac{20}{2}[2(5) + 19(3)]$ (A1)\n$S_{20} = 670$ (A1) [5 marks]",
                "subtopics": ["Arithmetic sequences and series"],
                "topic": "Number and algebra",
            },
        },
        # Geometric Sequences - Different approach: finding middle terms
        {
            "role": "User",
            "content": "Three numbers form a geometric sequence. Their sum is 26 and their product is 216. Find the three numbers.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Three numbers form a geometric sequence. Their sum is 26 and their product is 216. Find the three numbers.",
                "marks": 6,
                "markscheme": "Let the numbers be $\\frac{a}{r}$, $a$, $ar$ (M1)\n$\\frac{a}{r} + a + ar = 26$ and $\\frac{a}{r} \\cdot a \\cdot ar = a^3 = 216$ (A1)\n$a = 6$ (A1)\n$\\frac{6}{r} + 6 + 6r = 26$, so $\\frac{1}{r} + 1 + r = \\frac{13}{3}$ (A1)\n$3 + 3r + 3r^2 = 13r$, so $3r^2 - 10r + 3 = 0$ (A1)\n$r = 3$ or $r = \\frac{1}{3}$: numbers are $2, 6, 18$ (A1) [6 marks]",
                "subtopics": ["Geometric sequences and series"],
                "topic": "Number and algebra",
            },
        },
        # Financial Applications - Different approach: depreciation
        {
            "role": "User",
            "content": "A car depreciates at 15% per year. If it's worth $18,000 after 3 years, what was its original value?",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "A car depreciates at 15% per year. If it's worth $18,000 after 3 years, what was its original value?",
                "marks": 3,
                "markscheme": "$V_0(1-0.15)^3 = 18000$ (M1)\n$V_0(0.85)^3 = 18000$ (A1)\n$V_0 = \\frac{18000}{0.614125} = \\$29,297$ (A1) [3 marks]",
                "subtopics": ["Financial applications"],
                "topic": "Number and algebra",
            },
        },
        # Logarithms - Different approach: exponential equation
        {
            "role": "User",
            "content": "Solve $3^{2x-1} = 5^{x+2}$ for $x$, giving your answer to 3 significant figures.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Solve $3^{2x-1} = 5^{x+2}$ for $x$, giving your answer to 3 significant figures.",
                "marks": 4,
                "markscheme": "Taking logarithms: $(2x-1)\\ln 3 = (x+2)\\ln 5$ (M1)\n$2x\\ln 3 - \\ln 3 = x\\ln 5 + 2\\ln 5$ (A1)\n$x(2\\ln 3 - \\ln 5) = \\ln 3 + 2\\ln 5$ (A1)\n$x = \\frac{\\ln 3 + 2\\ln 5}{2\\ln 3 - \\ln 5} = 4.11$ (A1) [4 marks]",
                "subtopics": ["Logarithms"],
                "topic": "Number and algebra",
            },
        },
        # Laws of Exponents - Different approach: equation solving
        {"role": "User", "content": "If $2^x \\cdot 4^{x-1} = 8^{x+1}$, find the value of $x$."},
        {
            "role": "Chatbot",
            "content": {
                "content": "If $2^x \\cdot 4^{x-1} = 8^{x+1}$, find the value of $x$.",
                "marks": 4,
                "markscheme": "$2^x \\cdot (2^2)^{x-1} = (2^3)^{x+1}$ (M1)\n$2^x \\cdot 2^{2x-2} = 2^{3x+3}$ (A1)\n$2^{x+2x-2} = 2^{3x+3}$ (A1)\n$3x-2 = 3x+3$: no solution (A1) [4 marks]",
                "subtopics": ["Laws of exponents and logs"],
                "topic": "Number and algebra",
            },
        },
        # Infinite Geometric Series - Different approach: repeating decimal
        {
            "role": "User",
            "content": "Express the recurring decimal $0.\\overline{27}$ as a fraction in its simplest form.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Express the recurring decimal $0.\\overline{27}$ as a fraction in its simplest form.",
                "marks": 4,
                "markscheme": "$0.\\overline{27} = 0.27 + 0.0027 + 0.000027 + ...$ (M1)\n$= \\frac{27}{100} + \\frac{27}{10000} + \\frac{27}{1000000} + ...$ (A1)\n$= \\frac{27}{100}(1 + \\frac{1}{100} + \\frac{1}{10000} + ...)$ (A1)\n$= \\frac{27}{100} \\cdot \\frac{1}{1-\\frac{1}{100}} = \\frac{27}{99} = \\frac{3}{11}$ (A1) [4 marks]",
                "subtopics": ["Sum of infinite geometric sequence"],
                "topic": "Number and algebra",
            },
        },
        # Binomial Theorem - Different approach: specific term value
        {
            "role": "User",
            "content": "In the expansion of $(1+2x)^8$, find the term that is independent of $x$ when this expansion is multiplied by $(1-\\frac{1}{x})^3$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "In the expansion of $(1+2x)^8$, find the term that is independent of $x$ when this expansion is multiplied by $(1-\\frac{1}{x})^3$.",
                "marks": 6,
                "markscheme": "$(1+2x)^8 = \\sum_{r=0}^8 \\binom{8}{r}(2x)^r$ (M1)\n$(1-\\frac{1}{x})^3 = \\sum_{s=0}^3 \\binom{3}{s}(-\\frac{1}{x})^s$ (M1)\nGeneral term: $\\binom{8}{r}\\binom{3}{s}2^r(-1)^s x^{r-s}$ (A1)\nFor constant term: $r-s = 0$, so $r = s$ (A1)\nPossible pairs: $(0,0)$, $(1,1)$, $(2,2)$, $(3,3)$ (A1)\nConstant term: $\\binom{8}{0}\\binom{3}{0}2^0(-1)^0 + \\binom{8}{1}\\binom{3}{1}2^1(-1)^1 + \\binom{8}{2}\\binom{3}{2}2^2(-1)^2 + \\binom{8}{3}\\binom{3}{3}2^3(-1)^3 = 1 - 48 + 336 - 448 = -159$ (A1) [6 marks]",
                "subtopics": ["Binomial theorem"],
                "topic": "Number and algebra",
            },
        },
        # Permutations and Combinations - Different approach: restriction problem
        {
            "role": "User",
            "content": "A committee of 5 people is to be chosen from 6 men and 4 women. In how many ways can this be done if there must be more men than women on the committee?",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "A committee of 5 people is to be chosen from 6 men and 4 women. In how many ways can this be done if there must be more men than women on the committee?",
                "marks": 5,
                "markscheme": "More men than women: 3M+2W, 4M+1W, or 5M+0W (M1)\nCase 1: $\\binom{6}{3}\\binom{4}{2} = 20 \\times 6 = 120$ (A1)\nCase 2: $\\binom{6}{4}\\binom{4}{1} = 15 \\times 4 = 60$ (A1)\nCase 3: $\\binom{6}{5}\\binom{4}{0} = 6 \\times 1 = 6$ (A1)\nTotal: $120 + 60 + 6 = 186$ (A1) [5 marks]",
                "subtopics": ["Permutations and combinations"],
                "topic": "Number and algebra",
            },
        },
        # Partial Fractions - Different approach: repeated linear factor
        {"role": "User", "content": "Express $\\frac{3x^2-5x+7}{(x-1)^2(x+2)}$ in partial fractions."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Express $\\frac{3x^2-5x+7}{(x-1)^2(x+2)}$ in partial fractions.",
                "marks": 6,
                "markscheme": "$\\frac{3x^2-5x+7}{(x-1)^2(x+2)} = \\frac{A}{x-1} + \\frac{B}{(x-1)^2} + \\frac{C}{x+2}$ (M1)\n$3x^2-5x+7 = A(x-1)(x+2) + B(x+2) + C(x-1)^2$ (A1)\n$x=1: 5 = 3B$, so $B = \\frac{5}{3}$ (A1)\n$x=-2: 25 = 9C$, so $C = \\frac{25}{9}$ (A1)\nCoefficient of $x^2$: $3 = A + C$, so $A = 3 - \\frac{25}{9} = \\frac{2}{9}$ (A1)\n$\\frac{2/9}{x-1} + \\frac{5/3}{(x-1)^2} + \\frac{25/9}{x+2}$ (A1) [6 marks]",
                "subtopics": ["Partial fractions"],
                "topic": "Number and algebra",
            },
        },
        # Complex Numbers - Different approach: division
        {
            "role": "User",
            "content": "If $z_1 = 2-3i$ and $z_2 = 1+4i$, find $\\frac{z_1}{z_2}$ in the form $a+bi$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "If $z_1 = 2-3i$ and $z_2 = 1+4i$, find $\\frac{z_1}{z_2}$ in the form $a+bi$.",
                "marks": 4,
                "markscheme": "$\\frac{z_1}{z_2} = \\frac{2-3i}{1+4i} \\times \\frac{1-4i}{1-4i}$ (M1)\n$= \\frac{(2-3i)(1-4i)}{(1+4i)(1-4i)}$ (A1)\n$= \\frac{2-8i-3i+12i^2}{1-16i^2} = \\frac{-10-11i}{17}$ (A1)\n$= -\\frac{10}{17} - \\frac{11}{17}i$ (A1) [4 marks]",
                "subtopics": ["Complex numbers"],
                "topic": "Number and algebra",
            },
        },
        # Polar Form - Different approach: multiplication in polar form
        {
            "role": "User",
            "content": "If $z_1 = 2e^{i\\pi/4}$ and $z_2 = 3e^{i\\pi/6}$, find $z_1z_2$ and express in rectangular form.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "If $z_1 = 2e^{i\\pi/4}$ and $z_2 = 3e^{i\\pi/6}$, find $z_1z_2$ and express in rectangular form.",
                "marks": 4,
                "markscheme": "$z_1z_2 = 2e^{i\\pi/4} \\times 3e^{i\\pi/6} = 6e^{i(\\pi/4 + \\pi/6)}$ (M1)\n$= 6e^{i5\\pi/12}$ (A1)\n$= 6(\\cos\\frac{5\\pi}{12} + i\\sin\\frac{5\\pi}{12})$ (A1)\n$= 6(\\frac{\\sqrt{6}-\\sqrt{2}}{4} + i\\frac{\\sqrt{6}+\\sqrt{2}}{4}) = \\frac{3(\\sqrt{6}-\\sqrt{2})}{2} + i\\frac{3(\\sqrt{6}+\\sqrt{2})}{2}$ (A1) [4 marks]",
                "subtopics": ["Polar and Euler form"],
                "topic": "Number and algebra",
            },
        },
        # Complex Roots - Different approach: cubic with known rational root
        {"role": "User", "content": "Find all roots of $z^3 - 2z^2 + 4z - 8 = 0$."},
        {
            "role": "Chatbot",
            "content": {
                "content": "Find all roots of $z^3 - 2z^2 + 4z - 8 = 0$.",
                "marks": 5,
                "markscheme": "Try $z = 2$: $8 - 8 + 8 - 8 = 0$  (A1)\n$(z-2)$ is a factor: $z^3 - 2z^2 + 4z - 8 = (z-2)(z^2+4)$ (A1)\n$z^2 + 4 = 0$ gives $z^2 = -4$ (A1)\n$z = \\pm 2i$ (A1)\nRoots: $z = 2, 2i, -2i$ (A1) [5 marks]",
                "subtopics": ["Complex roots of polynomials"],
                "topic": "Number and algebra",
            },
        },
        # Proof by Induction - Different approach: inequality
        {
            "role": "User",
            "content": "Prove by mathematical induction that $2^n > n^2$ for all integers $n \\geq 5$.",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "Prove by mathematical induction that $2^n > n^2$ for all integers $n \\geq 5$.",
                "marks": 6,
                "markscheme": "Base case $n=5$: $2^5 = 32 > 25 = 5^2$  (A1)\nAssume true for $n=k$: $2^k > k^2$ (M1)\nProve for $n=k+1$: $2^{k+1} = 2 \\cdot 2^k > 2k^2$ (A1)\nNeed to show $2k^2 > (k+1)^2 = k^2 + 2k + 1$ (M1)\nThis requires $k^2 > 2k + 1$, or $k^2 - 2k - 1 > 0$ (A1)\nFor $k \\geq 5$: $k^2 - 2k - 1 = (k-1)^2 - 2 \\geq 16 - 2 = 14 > 0$ \nTherefore $2^{k+1} > (k+1)^2$ and result holds for all $n \\geq 5$ (A1) [6 marks]",
                "subtopics": ["Proof by induction"],
                "topic": "Number and algebra",
            },
        },
        # Systems of Linear Equations - Different approach: parameter-dependent system
        {
            "role": "User",
            "content": "For what values of $k$ does the system $x + 2y = 3$, $2x + ky = 5$ have: (a) a unique solution, (b) no solution, (c) infinitely many solutions?",
        },
        {
            "role": "Chatbot",
            "content": {
                "content": "For what values of $k$ does the system $x + 2y = 3$, $2x + ky = 5$ have: (a) a unique solution, (b) no solution, (c) infinitely many solutions?",
                "marks": 6,
                "markscheme": "Coefficient matrix: $\\begin{pmatrix} 1 & 2 \\\\ 2 & k \\end{pmatrix}$, det $= k - 4$ (M1)\n(a) Unique solution when det $\\neq 0$: $k \\neq 4$ (A1)\n(b) From equation 1: $x = 3 - 2y$. Substitute: $2(3-2y) + ky = 5$ (A1)\n$6 - 4y + ky = 5$, so $(k-4)y = -1$ (A1)\nIf $k = 4$: $0 \\cdot y = -1$, which is impossible: no solution (A1)\n(c) For infinitely many solutions, need $k = 4$ and consistent equations, but this gives no solution, so no value of $k$ gives infinitely many solutions (A1) [6 marks]",
                "subtopics": ["Systems of linear equations"],
                "topic": "Number and algebra",
            },
        },
    ]
}


def normalize_spaces(text):
    """
    Normalize leading spaces and remove unnecessary indentation in multi-line strings.
    Keeps line breaks, trims each line.
    """
    lines = text.strip().splitlines()
    cleaned_lines = [line.strip() for line in lines]
    return "\n".join(cleaned_lines)


def convert_dataset_format(nested_dataset):
    """
    Convert nested dataset format to flattened format
    """
    converted_messages = []

    for message in nested_dataset["messages"]:
        if message["role"] == "System":
            # Keep system messages as is
            converted_messages.append({"role": "System", "content": message["content"]})
        elif message["role"] == "User":
            # Keep user messages as is
            converted_messages.append({"role": "User", "content": "Numbers and Algebra"})
        elif message["role"] == "Chatbot":
            # Flatten the nested content structure
            content_dict = message["content"]

            # Create the flattened content string
            flattened_content = f"""
            content: {content_dict['content']}
            marks: {content_dict['marks']}
            markscheme: {content_dict['markscheme']}
            subtopics: {content_dict['subtopics']}
            topic: {content_dict['topic']}
            """

            # Create the flattened message
            flattened_message = {"role": "Chatbot", "content": normalize_spaces(flattened_content)}

            converted_messages.append(flattened_message)

    output = {"messages": converted_messages}
    return output


with open("output.json", "w") as f:
    json.dump(convert_dataset_format(eval_data), f)
