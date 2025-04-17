# src/ontology/visualizer.py

from pyvis.network import Network
from owlready2 import Thing

def visualize(classes, object_properties, individuals, filename="ontology.html"):
    net = Network(width="100%", height="100vh", cdn_resources='in_line', notebook=False, directed=True)
    net.repulsion(node_distance=300, spring_length=200, central_gravity=0.1)

    added_nodes = set()

    for cls_name, cls_obj in classes.items():
        node_id = f"class_{cls_name}"
        if node_id not in added_nodes:
            net.add_node(node_id, label=cls_name, shape='box', color='lightblue',
                         title=f"Class: {cls_name}", group='class')
            added_nodes.add(node_id)

        for parent_cls in cls_obj.is_a:
            if isinstance(parent_cls, Thing.__class__):
                parent_id = f"class_{parent_cls.name}"
                if parent_id not in added_nodes:
                    net.add_node(parent_id, label=parent_cls.name, shape='box', color='lightblue',
                                 title=f"Class: {parent_cls.name}", group='class')
                    added_nodes.add(parent_id)
                net.add_edge(parent_id, node_id, label="subclass_of", arrows='to', width=2, color='gray', group='edge_class')

    for ind_name, ind_obj in individuals.items():
        cls_name = ind_obj.is_a[0].name
        net.add_node(f"ind_{ind_name}", label=ind_name, shape='dot', color='yellow',
                     title=f"Individual of class: {cls_name}", group='individual')
        net.add_edge(f"class_{cls_name}", f"ind_{ind_name}", arrows='to', color='black', width=2, group='edge_ind')

    prop_counter = 0
    for prop_name, _ in object_properties.items():
        for subj in individuals.values():
            for obj in getattr(subj, prop_name, []):
                prop_counter += 1
                prop_node_id = f"prop_{prop_name}_{prop_counter}"
                net.add_node(prop_node_id, label=prop_name, shape='triangle', color='tomato',
                             title=f"{prop_name}: {subj.name} → {obj.name}", group='property')
                net.add_edge(f"ind_{subj.name}", prop_node_id, arrows='to', color='orange', width=2, group='edge_prop')
                net.add_edge(prop_node_id, f"ind_{obj.name}", arrows='to', color='orange', width=2, group='edge_prop')

    html_content = net.generate_html()

    # Стили и JS для управления слоями
    style_patch = """
    <style>
    html, body {
        width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden;
    }
    #mynetwork {
        width: 100vw !important; height: 100vh !important; border: none; position: absolute;
        top: 0; left: 0; z-index: 0;
    }
    .layer-controls {
        position: absolute; top: 10px; left: 10px; z-index: 10;
        background: white; padding: 10px; border: 1px solid #ccc; border-radius: 6px;
    }
    </style>
    """

    controls_js = """
    <script>
    function toggleGroup(groupName) {
        let nodes = network.body.data.nodes.get();
        let edges = network.body.data.edges.get();

        nodes.forEach(n => {
            if (n.group === groupName) {
                n.hidden = !n.hidden;
                network.body.data.nodes.update(n);
            }
        });

        edges.forEach(e => {
            if (e.group === "edge_" + groupName) {
                e.hidden = !e.hidden;
                network.body.data.edges.update(e);
            }
        });
    }

    network.once("stabilizationIterationsDone", function () {
        network.fit({ animation: { duration: 1000, easingFunction: "easeInOutQuad" } });
    });
    </script>

    <div class=\"layer-controls\">
        <button onclick=\"toggleGroup('class')\">Toggle Classes</button>
        <button onclick=\"toggleGroup('individual')\">Toggle Individuals</button>
        <button onclick=\"toggleGroup('property')\">Toggle Properties</button>
    </div>
    """

    final_html = html_content.replace("</head>", style_patch + "\n</head>")
    final_html = final_html.replace("</body>", controls_js + "\n</body>")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_html)
