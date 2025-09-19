from harmless_search import harmlessSearch

"""
I: instance
C: confidentiality constraints
F_O: owner fragment
F_S: server fragment
Sigma_T: set of TGDs
res: result
print(Conflict) as a safeguard (if conflict occurres during procedure)
"""


# -----------------------------------
# Test 1: with sensitive information
# -----------------------------------
I1 = {("Illness", "mary", "aids")}
C1 = [("Illness", "X", "aids")]

F_O1, F_S1 = set(), set()
res1 = harmlessSearch(I1, C1, [], [], F_O1, F_S1)

print("Test 1:")
print("Owner Fragment F_O:", res1[0])
print("Server Fragment F_S:", res1[1])
print("Conflict:", res1[2])
print("----------------------------------------------------------------------------------------------------------")

# --------------------------------------
# Test 2: without sensitive information
# --------------------------------------
I2 = {("Illness", "pete", "flu"), ("Illness", "mary", "myopia")}
C2 = [("Illness", "X", "aids")]

F_O2, F_S2 = set(), set()
res2 = harmlessSearch(I2, C2, [], [], F_O2, F_S2)

print("Test 2:")
print("Owner Fragment F_O:", res2[0])
print("Server Fragment F_S:", res2[1])
print("Conflict:", res2[2])
print("----------------------------------------------------------------------------------------------------------")

# -----------------------------------------------
# Test 3: with and without sensitive information
# -----------------------------------------------
I3 = {
    ("Illness", "mary", "aids"),
    ("Illness", "pete", "flu"),
    ("Illness", "lisa", "covid")
}
C3 = [
    ("Illness", "X", "aids"),
    ("Illness", "Y", "covid")
    ]

F_O3, F_S3 = set(), set()
res3 = harmlessSearch(I3, C3, [], [], F_O3, F_S3)

print("Test 3:")
print("Owner Fragment F_O:", res3[0])
print("Server Fragment F_S:", res3[1])
print("Conflict:", res3[2])
print("----------------------------------------------------------------------------------------------------------")

# -----------------------------------------------
# Test 4: with and without sensitive information
# -----------------------------------------------
I4 = {
    ("Illness", "mary", "aids"),
    ("Illness", "tom", "cancer"),
    ("Illness", "pete", "flu"),
    ("Illness", "lisa", "covid")
}
C4 = [
    ("Illness", "X", "aids"),
    ("Illness", "Y", "cancer"),
    ("Illness", "Z", "covid")
]

F_O4, F_S4 = set(), set()
res4 = harmlessSearch(I4, C4, [], [], F_O4, F_S4)

print("Test 4")
print("Owner Fragment F_O:", res4[0])
print("Server Fragment F_S:", res4[1])
print("Conflict:", res4[2])
print("----------------------------------------------------------------------------------------------------------")

# ----------------------------------------------------------------
# Test 5: with TGD "if someone has a flu, this person needs care"
# ----------------------------------------------------------------
Sigma_T5 = [
    (
        [("Illness", "X", "flu")],  # body
        [("NeedsCare", "X")]        # head
    )
]
I5 = {("Illness", "Mary", "flu")}
C5 = []

F_O5, F_S5 = set(), set()
res5 = harmlessSearch(I5, C5, Sigma_T5, [], F_O5, F_S5)

print("Test 5")
print("Owner Fragment F_O:", res5[0])
print("Server Fragment F_S:", res5[1])
print("Conflict:", res5[2])
print("----------------------------------------------------------------------------------------------------------")

# -----------------------------------------------------
# Test 6: with and without sensitive information + TGD
# -----------------------------------------------------
Sigma_T6 = [
    (
        [("Illness", "X", "flu")],
        [("NeedsCare", "X")]
    )
]
I6 = {
    ("Illness", "pete", "flu"), 
    ("Illness", "mary", "myopia"), 
    ("Illness", "tom", "cancer"), 
    ("Illness", "lisa", "covid")
    }
C6 = [("NeedsCare", "pete")]

F_O6, F_S6 = set(), set()
res6 = harmlessSearch(I6, C6, Sigma_T6, [], F_O6, F_S6)

print("Test 6")
print("Owner Fragment F_O:", res6[0])
print("Server Fragment F_S:", res6[1])
print("Conflict:", res6[2])
