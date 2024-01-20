# Hackday 2024: Blueprint mirage

## Challenge information

**Category**: Forensic

**Description**: This challenge is about the analysis of a gcode file. The goal is to find the flag hidden in the file.

## Solution

**Step 1: Initial analysis**

We are given a gcode file. This file is a list of instructions for a 3D printer.
The first step is to put the file in a gcode viewer. We can use [Cura](https://ultimaker.com/software/ultimaker-cura) for example.
We can see that the file contains a 3D model of the Hackday logo, but no information about the flag.

**Step 2: Deeper analysis**

We can start to analyze the file structure.
We can see that the file contains a lot of `G1` instructions. These instructions are used to move the printer head.
Each instruction type start with a specific letter. We can find the explication of each instruction type [here](https://www.autodesk.com/products/fusion-360/blog/cnc-programming-fundamentals-g-code/).
![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f7c89256-92c9-4037-9966-4edb1103dc26)


In the beginning of the file, we can see a lot of `F` instructions with three digits after that aren't explained. We can assume that these instructions are used to hide the flag.

**Step 3: Extracting the flag**

We can expect that these three digits are used to hide the flag as ASCII characters. We can extract these digits and convert them to ASCII characters.
We can use the following bash command to extract the digits:
```bash
grep -E '\bF[01][0-9]{2}\b' gcode.txt | sed 's/F//' | awk '{printf "%c", $1}'; echo
```

### Flag

We can see that the flag is hidden in the file:
`HACKDAY{Pr3Ss_F_7O_prAY}`

## Creator

* Name: [Louis GAMBART](https://linkedin.com/in/louis-gambart)

## References

* [Gcode instructions](https://www.autodesk.com/products/fusion-360/blog/cnc-programming-fundamentals-g-code/)
* [Cura](https://ultimaker.com/software/ultimaker-cura)
* [Gcode viewer](https://gcode.ws/)
