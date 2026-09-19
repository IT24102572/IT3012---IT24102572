class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def tell_fact(self, fact_string: str):
        """Add a unique fact to the KB."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list: list, conclusion_string: str):
        """Store rules as tuples: (premise_list, conclusion_string)."""
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        """Empty the facts set."""
        self.facts.clear()

    def forward_chain(self):
        """
        Executes Data-Driven Forward Chaining using Modus Ponens until
        no new facts can be deduced.
        """
        new_facts_added = True
        while new_facts_added:
            new_facts_added = False
            for premises, conclusion in self.rules:
                if conclusion not in self.facts:
                    # Modus Ponens Check: If ALL premises exist in facts
                    if all(p in self.facts for p in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True