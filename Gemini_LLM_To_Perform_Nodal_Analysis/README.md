TOOLS: Gemini LLM
## Gemeni LLM 

Software components: Thonny, Gemini 2.5 flash


## Text-based Input
```Python
google.generativeai as genai
genai.configure(api_key="api-key")
 
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("""You are an ELE 231 circuit tutor. You are given an LTspice schematic IMAGE.

The circuit contains ONLY:
- resistors
- independent voltage sources
- independent current sources
- wires and ground

Task:
1) Identify the reference (ground) node (the ground symbol).
2) Assign node names consistently (n1, n2, n3, ...) to every distinct electrical node you see (every unique junction/wire group).
3) Perform NODAL ANALYSIS:
   - Write KCL at every non-ground node.
   - If a voltage source connects two non-ground nodes, form a supernode and add the voltage constraint equation.
   - Use these conventions:
     * Resistor current from node a to b: (Va - Vb)/R
     * Voltage source: Va - Vb = V
     * Current source arrow from a to b means current leaving node a and entering node b.
4) Solve the system and provide the final node voltages relative to ground.

Output format (required):
A) Node labeling (describe which parts of the schematic are n1, n2, ... in plain words)
B) Unknowns list: V(n1), V(n2), ...
C) KCL equations (symbolic, one per node / supernode)
D) Solved node voltages (rounded to 4 decimals):
   V(n1)=...
   V(n2)=...
   ...

Quality checks before final answer:
- Confirm the number of independent equations equals the number of unknown node voltages.
- Substitute your final voltages into at least one KCL equation and state whether it balances (approximately).
- Do not invent components or connections that are not visible in the image.
Treat any wire segment connected by a junction dot as the same node. Any crossing without a junction dot is NOT connected.

Evaluate this SPICE netlist: 
V1 N001 0 10
R1 N002 0 5
R2 N003 0 2.5
R3 P001 N001 2
R4 N002 P001 3
I1 0 N003 0.8
R5 N003 N002 10
""")

print(response.text)


```
- This code reads the spice net-list and returns the values of the voltages. We used gemini 2.5 flash to create the api keys. It accepts a spice netlist format text input, performs nodal analysis with correct math, and provides structured, text input output that explains the solving procedure. 


This graph shows the usage for this code
![[20260302_15h15m01s_grim.png]]

Here is the markdown table:
![[Screenshot 2026-03-02 at 3.21.10 PM.png]]


```


## Image-based Input

```Python
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyAvGutRwpdlx-3tHP84D3qMdLfSvAK_XdQ")
 
model = genai.GenerativeModel("gemini-2.5-flash")
img = Image.open("Circuit_1.png")
response = model.generate_content(
    ["""You are an ELE 231 circuit tutor. You are given an LTspice schematic IMAGE.

The circuit contains ONLY:
- resistors
- independent voltage sources
- independent current sources
- wires and ground

Task:
1) Identify the reference (ground) node (the ground symbol).
2) Assign node names consistently (n1, n2, n3, ...) to every distinct electrical node you see (every unique junction/wire group).
3) Perform NODAL ANALYSIS:
   - Write KCL at every non-ground node.
   - If a voltage source connects two non-ground nodes, form a supernode and add the voltage constraint equation.
   - Use these conventions:
     * Resistor current from node a to b: (Va - Vb)/R
     * Voltage source: Va - Vb = V
     * Current source arrow from a to b means current leaving node a and entering node b.
4) Solve the system and provide the final node voltages relative to ground.

Output format (required):
A) Node labeling (describe which parts of the schematic are n1, n2, ... in plain words)
B) Unknowns list: V(n1), V(n2), ...
C) KCL equations (symbolic, one per node / supernode)
D) Solved node voltages (rounded to 4 decimals):
   V(n1)=...
   V(n2)=...
   ...

Quality checks before final answer:
- Confirm the number of independent equations equals the number of unknown node voltages.
- Substitute your final voltages into at least one KCL equation and state whether it balances (approximately).
- Do not invent components or connections that are not visible in the image.
Treat any wire segment connected by a junction dot as the same node. Any crossing without a junction dot is NOT connected.""",
        img
    ]
    )

print(response.text)


```

- This code reads an image based circuit schematic, performs nodal analysis with correct math, and provides structured, text input output that explains the solving procedure. We used gemini 2.5 flash to create the api keys. 


This is the usage based on the code
![[20260302_15h21m23s_grim.png]]

Here is the markdown table:
![[Screenshot 2026-03-02 at 3.21.10 PM 1.png]]
