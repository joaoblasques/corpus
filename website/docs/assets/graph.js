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
        function _lighten(hex, f) {              // mix a hex color toward the page bg (#faf8f2)
          var b = { r: 250, g: 248, b: 242 };
          var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), bl = parseInt(hex.slice(5, 7), 16);
          function mix(c, t) { return Math.round(c + (t - c) * f); }
          function h2(x) { return ("0" + x.toString(16)).slice(-2); }
          return "#" + h2(mix(r, b.r)) + h2(mix(g, b.g)) + h2(mix(bl, b.b));
        }
        function _depthTier(d) {                  // 0=thin ... 3=deep -> lighten fraction
          if (d < 300) return 0.6;
          if (d < 800) return 0.4;
          if (d < 1800) return 0.2;
          return 0.0;
        }
        data.nodes.forEach(function (n) {
          var base = GROUP_COLORS[n.group] || "#8a8a7a";
          if (n.hub) {
            n.color = { background: base, border: base, highlight: { background: base, border: "#c8862a" } };
            n.shape = "dot";
            n.value = n.value || 52;
            n.label = n.label + " · " + (n.sources || 0) + " sources";
            n.font = { size: 22, face: "Lora, Georgia, serif", color: "#3a3a32", strokeWidth: 5, strokeColor: "#faf8f2" };
            n.borderWidth = 3;
          } else {
            var c = _lighten(base, _depthTier(n.depth || 0));   // pale = thin page, saturated = deep
            n.color = { background: c, border: c, highlight: { background: c, border: "#c8862a" } };
            n.shape = "dot";
            n.value = Math.max(n.degree || 1, 1);               // size = real connection count
            n.font = { size: 13, face: "Inter, sans-serif", color: "#4a4a42" };
            if ((n.degree || 0) <= 1) {                          // orphan: only its spoke to the hub
              n.borderWidth = 1;
              n.shapeProperties = { borderDashes: [2, 3] };
              n.color.border = "#b8b0a0";
            }
          }
        });
        var nodes = new vis.DataSet(data.nodes);
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge
            ? { color: "rgba(200,134,42,0.55)", highlight: "#c8862a" }   // cross-domain bridge: warm accent
            : { color: "rgba(120,120,105,0.22)", highlight: "#c8862a" };  // same-domain: faint grey
          return { from: e.from, to: e.to, color: col, width: e.bridge ? 1.2 : 0.6 };
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
