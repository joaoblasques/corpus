/* Corpus knowledge graph — hubs (domains) · spokes (pages) · connections (wikilinks).
   Data is regenerated from the real corpus at every build (see hooks/corpus_graph.py).
   Instant-navigation aware (Material's document$), large-graph tuned. */
(function () {
  var GROUP_COLORS = {
    "ai-engineering":      "#5a7a5a",
    "data-engineering":    "#c8862a",
    "mlops":               "#b5651d",
    "software-engineering":"#5a6f8a",
    "ai-business":         "#b89020",
    "blockchain":          "#8a6f9a",
    "productivity":        "#7a9a5a"
  };

  function render() {
    var el = document.getElementById("corpus-graph");
    if (!el || el.dataset.rendered === "1" || typeof vis === "undefined") return;
    el.dataset.rendered = "1";
    fetch("assets/graph-data.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        data.nodes.forEach(function (n) {
          var c = GROUP_COLORS[n.group] || "#8a8a7a";
          n.color = { background: c, border: c, highlight: { background: c, border: "#c8862a" } };
          n.shape = "dot";
          if (n.hub) {
            n.value = n.value || 52;
            n.font = { size: 22, face: "Lora, Georgia, serif", color: "#3a3a32", strokeWidth: 5, strokeColor: "#faf8f2" };
            n.borderWidth = 3;
          } else {
            n.value = 9;
            n.font = { size: 13, face: "Inter, sans-serif", color: "#4a4a42" };
          }
        });
        var nodes = new vis.DataSet(data.nodes);
        var edges = new vis.DataSet(data.edges.map(function (e) {
          return { from: e.from, to: e.to, color: { color: "rgba(120,120,105,0.22)", highlight: "#c8862a" } };
        }));
        new vis.Network(el, { nodes: nodes, edges: edges }, {
          nodes: { scaling: { min: 9, max: 52 } },
          edges: { smooth: { type: "continuous" }, width: 0.6 },
          physics: {
            barnesHut: { gravitationalConstant: -3600, springLength: 155, springConstant: 0.02, damping: 0.45, avoidOverlap: 0.25 },
            stabilization: { iterations: 220 }
          },
          interaction: { hover: true, tooltipDelay: 120, hideEdgesOnDrag: true },
          layout: { improvedLayout: false }
        });
      })
      .catch(function () {});
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(render);
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
})();
