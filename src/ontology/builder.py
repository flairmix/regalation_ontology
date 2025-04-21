from owlready2 import get_ontology, Thing, ObjectProperty, DataProperty, types

class OntologyBuilder:
    def __init__(self, base_uri="http://example.org/ontology#"):
        self.onto = get_ontology(base_uri)
        self.classes = {}
        self.object_properties = {}
        self.data_properties = {}
        self.individuals = {}

    def add_class(self, class_name, parent_class=Thing):
        if class_name not in self.classes:
            with self.onto:
                new_class = types.new_class(class_name, (parent_class,))
            self.classes[class_name] = new_class
        return self.classes[class_name]

    def add_object_property(self, property_name, domain, range_):
        if property_name not in self.object_properties:
            with self.onto:
                new_property = types.new_class(property_name, (ObjectProperty,))
                new_property.domain = [self.classes[domain]]
                new_property.range = [self.classes[range_]]
            self.object_properties[property_name] = new_property
        return self.object_properties[property_name]

    def add_individual(self, class_name, individual_name):
        with self.onto:
            individual = self.classes[class_name](individual_name)
        self.individuals[individual_name] = individual
        return individual

    def relate_individuals(self, subject, predicate, obj):
        getattr(subject, predicate).append(obj)

    def save(self, filename):
        self.onto.save(file=filename, format="rdfxml")

    def get_entities(self):
        return self.classes, self.object_properties, self.individuals
    
    def add_data_property(self, property_name, domain, dtype=str): 
        if property_name not in self.data_properties:
            with self.onto:
                new_property = types.new_class(property_name, (DataProperty,))
                new_property.domain = [self.classes[domain]]
                new_property.range = [dtype]
            self.data_properties[property_name] = new_property
        return self.data_properties[property_name]
    
    def assign_data_property(self, subject, property_name, value): 
        """Присвоить значение data property для индивидуала."""
        if property_name not in self.data_properties:
            raise ValueError(f"DataProperty '{property_name}' not found. Call add_data_property first.")
        getattr(subject, property_name).append(value)
