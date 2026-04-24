from typing import List, Dict, Optional

class KnowledgeGraphSim:
    """
    A Python module that simulates the Neo4j Knowledge Graph logic using a 
    dictionary-based adjacency list for the MVP, allowing for Prerequisite checking.
    """
    def __init__(self):
        # Format: { "Concept": { "prerequisites": ["ConceptA", "ConceptB"], "content": "..." } }
        self.graph = {
            "Basic Finance": {
                "prerequisites": [],
                "content": "Basic Finance covers the fundamental principles of managing money, including saving, investing, and budgeting."
            },
            "Budgeting": {
                "prerequisites": ["Basic Finance"],
                "content": "Budgeting is the process of creating a plan to spend your money, helping you determine in advance whether you will have enough money to do the things you need to do or would like to do."
            },
            "Interest Rates": {
                "prerequisites": ["Basic Finance"],
                "content": "An interest rate is the amount charged, expressed as a percentage of principal, by a lender to a borrower for the use of assets."
            },
            "Compound Interest": {
                "prerequisites": ["Interest Rates"],
                "content": "Compound interest is the addition of interest to the principal sum of a loan or deposit, or in other words, interest on interest."
            },
            "Investing": {
                "prerequisites": ["Basic Finance", "Compound Interest"],
                "content": "Investing is the act of allocating resources, usually money, with the expectation of generating an income or profit."
            }
        }

    def get_prerequisites(self, concept: str) -> List[str]:
        if concept in self.graph:
            return self.graph[concept]["prerequisites"]
        return []

    def get_content(self, concept: str) -> Optional[str]:
        if concept in self.graph:
            return self.graph[concept]["content"]
        return None

    def check_prerequisites_met(self, concept: str, mastered_concepts: List[str]) -> bool:
        """
        Checks if all prerequisites for a given concept are in the list of mastered_concepts.
        """
        prereqs = self.get_prerequisites(concept)
        return all(p in mastered_concepts for p in prereqs)

# Singleton instance for the MVP
kg = KnowledgeGraphSim()
