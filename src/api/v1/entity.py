from abc import abstractmethod
from operators import ComparisonOperator


class EntityProperty:
    pass


class Comparable:
    
    @abstractmethod
    def compare(self, property: EntityProperty, op: ComparisonOperator) -> bool:
        """
        This abstract method should be used to compare an entity with a give entity property and a comparison operator. The 
        method returns the truth value of the comparison.
        
        params:
        property (EntityProperty): An entity property the entity should compare to.
        
        returns:
        Boolean value according to the comparison result
        """
        pass


class Entity(Comparable):
    pass
    
    
EntityDescriptor = dict[str, str] # Key-value dictionary of Entitry's attribute name and its NLP query value

