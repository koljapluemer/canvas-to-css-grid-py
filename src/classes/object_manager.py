class ObjectManager:
    nodes = []
    edges = []

    @staticmethod
    def create_from_JSON(json_data):
        obj_manager = ObjectManager()
        obj_manager.nodes = json_data.get('nodes', [])
        obj_manager.edges = json_data.get('edges', [])
        return obj_manager
    
    def export_to_JSON(self):
        return {}
