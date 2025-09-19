############################################################################
####            A PROTOTYPE OF THE HARMLESS SEARCH ALGORITHM            ####
############################################################################

def safeTaintedness(egd) -> bool:
    """
    Function: 
        Check whether EGD is safe tainted
    
    Dummy version: 
        If...
        - ... the EGDs only equate constants --> safe
        - ... the EGDs contain variables --> unsafe
    """
    for term in egd:
        if isinstance(term, str) and term and term[0].isupper():
            return False
    return True
    
def isWardedTGD(tgd) -> bool:
    """
    Function:
        Check whether TGD is warded

    Dummy version:
        Check whether a body or head is present --> true
    
    Later:
        Analyze affected variables
    """
    try:
        body, head = tgd
        return bool(body) and bool(head)
    except Exception:
        return False

def checkAllEGDsSatisfied(I, sigH) -> bool:
    """
    Function:
        Check whether all EGDs from harmlessEGD in I are fulfilled
    
    Dummy version:
        Check whether I or sigH is empty --> true
    """
    if not sigH:
        return True
    if not I:
        return True
    return True # always true for dummy

def RelaxedWardedChase(instance, sigW):
    """
    Function:
        Relaxed Warded Chase
    
    Dummy version:
        Return input instance
    
    Later:
        Extension by applying warded TGDs
    """
    return set(instance)

def applyHarmlessEGDs(chase, sigH):
    """
    Function:
        Application of harmless EGDs to Relaxed Warded Chase
    
    Dummy version:
        Return input instance
    
    Later:
        Check whether EGDs are violated
    """
    return set(chase)

def applyHarmlessEGDs_to_fixpoint(chase, sigH, max_iters=10):
    """
    Function:
        Fixed point for EGDs (even if EGDs are fulfilled in I)
    
    Dummy version:
        Instance always unchanged
    """
    prev = None
    current = set(chase)
    it = 0
    while prev != current and it < max_iters:
        prev = set(current)
        current = applyHarmlessEGDs(current, sigH)
        it += 1
    return current

def t_isomorphic(phi, inst) -> bool:
    """
    Function:
        Check whether t-isomorphism exists between phi and an element in Inst
    
    Dummy version:
        Output true if phi is already contained exactly in inst
    
    Later:
        Extension to recognize isomorphic variants with zeros
    """
    return phi in inst

def chase_entails(chase, formula) -> bool:
    """
    Function: 
        Check whether chase |= formula
        - chase: set of facts (e.g., {("Illness","mary", "aids"), ...})
        - formula: tuple with constants or variables (uppercase letters)
    
    Dummy version: 
        Returns all substitutions that satisfy formula in chase (empty --> not satisfied)
    """
    if isinstance(formula, tuple):
        body = [formula]
    else:
        body = list(formula)

    return satisfying_assignments(chase, body)

def isAffectedPosition(literal) -> bool:
    """
    Function:
        Check whether literal is at affected position
    
    Dummy version: 
        Return false (no position is affected)
    
    Later:
        Analyze TGDs to mark affected positions if necessary
    """
    return False

def isConstant(literal) -> bool:
    """
    Function:
        Check whether literal is a constant, assuming that:
        - constants are strings that begin with lowercase letters
        - variables are strings that begin with uppercase letters
    """
    for term in literal[1:]:
        if isinstance(term, str) and term and term[0].isupper():
            return False
    return True


# ----------------
# HARMLESS SEARCH
# ----------------

def harmlessSearch(I, C, Sigma_T, Sigma_E, F_O, F_S):
    Sigma_H = [eta for eta in Sigma_E if safeTaintedness(eta)]
    Sigma_W = [sigma for sigma in Sigma_T if isWardedTGD(sigma)]

    EGDsSatisfiedInI = checkAllEGDsSatisfied(I, Sigma_H)

    Inst = []  # only used for TGD gaps

    # --- Relaxed Warded Chase ---
    Chase = RelaxedWardedChase(I | F_S, Sigma_W)
    if not EGDsSatisfiedInI:
        Chase = applyHarmlessEGDs(Chase, Sigma_H)

    # --- Remove existential quantifiers ---
    quantifier_free_C = [remove_existential(phi) for phi in C]

    # --- Check confidentiality constraints ---
    cc_violations = []
    for phi in quantifier_free_C:
        subs = chase_entails(Chase, phi)
        for theta in subs:
            inst = substitute([phi], theta)[0]
            # Collecting instantiated confidentiality constraints
            if phi in C and not t_isomorphic(inst, cc_violations):
                cc_violations.append(inst)


    # --- Move violations of confidentiality constraints in F_O and remove from I ---
    if cc_violations:
        F_O |= set(cc_violations)
        I = I - set(cc_violations)

    # --- Check warded TGDs (collect gaps in Inst) ---
    for tgd in Sigma_W:
        body, head = tgd_body(tgd), tgd_head(tgd)
        for a in satisfying_assignments(Chase, body):
            if not chase_entails(Chase, substitute(head, a)):
                phi_a = substitute(body, a)
                if not t_isomorphic(phi_a, Inst):
                    Inst.append(phi_a)

    # --- Abort ---
    if not Inst:
        F_S |= I
        return F_O, F_S, False  # success, no conflict

    # --- Branching ---
    conj = Inst[0]
    literals = literals_of(conj)

    if set(literals).issubset(F_S):
        return F_O, F_S, True  # conflict (all literals already on server)

    li = choose_literal(literals, I)

    if isAffectedPosition(li) and isConstant(li):
        return harmlessSearch(I - {li}, C, Sigma_T, Sigma_E, F_O, F_S)

    # Branch 1: moves literal to owner fragment
    F_O_prime = F_O | {li}
    I_prime = I - {li}
    if I_prime == I:
        return F_O, F_S, False
    res1 = harmlessSearch(I_prime, C, Sigma_T, Sigma_E, F_O_prime, F_S)
    if not res1[2]:
        return res1

    # Branch 2: moves literal to server fragment if conflict in branch 1
    F_S_prime = F_S | {li}
    I_prime = I - {li}
    if I_prime == I:
        return F_O, F_S, False
    res2 = harmlessSearch(I_prime, C, Sigma_T, Sigma_E, F_O, F_S_prime)
    return res2


# ------------------
# Support functions 
# ------------------

def remove_existential(phi):
    """
    Function:
        Remove existence quantifiers from formula
    
    Dummy version:
        No quantifiers used, which is why phi is returned unchanged
    """
    return phi

def tgd_body(tgd):
    """
    Function:
        Extract body from TGD
    """
    if isinstance(tgd, tuple) and len(tgd) == 2:
        return list(tgd[0])
    return []

def tgd_head(tgd):
    """
    Function:
        Extract head from TGD
    """
    if isinstance(tgd, tuple) and len(tgd) == 2:
        return list(tgd[1])
    return []

def satisfying_assignments(chase, body):
    """
    Function:
        Find all substitutions such that body satisfies chase
        - Chase: Set of facts, e.g., {("Illness","mary","aids"), ...}
        - Body: List of literals, e.g., [("Illness","X","aids")]
        Return: List of substitutions, e.g. [{"X": "mary"}]
    """
    assignments = [{}]
    for atom in body:
        pred, *args = atom
        new_assignments = []
        for fact in chase:
            if fact[0] != pred:
                continue
            for theta in assignments:
                theta_copy = dict(theta)
                match = True
                for fa, fo in zip(fact[1:], args):
                    if isinstance(fo, str) and fo and fo[0].isupper():
                        if fo in theta_copy and theta_copy[fo] != fa:
                            match = False
                            break
                        theta_copy[fo] = fa
                    else:
                        if fa != fo:
                            match = False
                            break
                if match:
                    new_assignments.append(theta_copy)
        assignments = new_assignments
        if not assignments:
            break
    return assignments

def substitute(formula, assignment):
    """
    Function:
        Apply a substitution to a formula
        - formula: List of literals, e.g., [("Illness","X","flu")]
        - assignment: Dict, e.g., {"X":"pete"}
        
        Return: New list of literals with replaced variables
    """
    new_formula = []
    for atom in formula:
        pred, *args = atom
        new_args = []
        for arg in args:
            if isinstance(arg, str) and arg in assignment:
                new_args.append(assignment[arg])
            else:
                new_args.append(arg)
        new_formula.append((pred, *new_args))
    return new_formula

def substitute_as_conjunction(phi, assignment):
    """
    Function:
        Replaces variables in phi and returns a conjunction (list)
    """
    if isinstance(phi, tuple):
        return substitute([phi], assignment)
    else:
        return substitute(list(phi), assignment)

def literals_of(conj):
    """
    Function:
        Decomposes a conjunction into its literals.
    
    Dummy version:
        If...
        - ... conj is a list of literals --> return the list
        - ... conj is a single literal (tuple) --> put it in a list
    """
    if isinstance(conj, list) or isinstance(conj, tuple) and conj and isinstance(conj[0], tuple):
        return list(conj)
    return [conj]

def choose_literal(literals, I):
    """
    Function:
        Select a literal from the literals that also appears in I
    Dummy version:
        Takes the first literal contained in I
        If no literal contained in I --> return first literal
    """
    for lit in literals:
        if lit in I and not (isAffectedPosition(lit) and isConstant(lit)):
            return lit
        
    for lit in literals:
        if lit in I:
            return lit
    return None

def canonicalize(phi):
    """
    Function:
        Atom remains an atom (tuple)
        Conjunction (list of atoms) becomes a frozenset(atoms)
    """
    if isinstance(phi, list):
        return frozenset(phi)
    return phi
