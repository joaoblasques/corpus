/* Corpus knowledge graph — "Archive" theme + diagnostic encodings + interactivity.
   Truthful rendering: node SIZE = connection count (degree), LIGHTNESS = page depth (word count),
   hub labels carry source counts, cross-domain "bridge" edges are accented, orphans (degree 1)
   get a dashed ring. Interactions: click a node for a summary (+ link to its GitHub source),
   search by title/alias, filter by domain/depth/orphan, and a grown-over-time slider (by each
   page's `created` date). Data is regenerated from the real corpus at every build — only titles +
   structure, never page text. */
(function () {
  var REPO = "https://github.com/joaoblasques/corpus/";

  // Muted, earthy per-domain palette. We DELETE the vis `group` property from nodes and colour
  // every node explicitly, so vis-network never falls back to its bright default group palette.
  var GROUP_COLORS = {
    "ai-engineering":       "#5f7d5a",
    "data-engineering":     "#bf8a3c",
    "mlops":                "#b06a3f",
    "software-engineering": "#6a7d9c",
    "ai-business":          "#a08a3c",
    "blockchain":           "#8a7aa2",
    "productivity":         "#7a955a",
    "trading":              "#4f8a7c"
  };

  function tokens() {
    var scheme = document.body.getAttribute("data-md-color-scheme");
    var dark = scheme === "slate";
    return {
      dark: dark,
      surface: dark ? "#232019" : "#fbf8f0",
      ink:     dark ? "#ece5d6" : "#2b2820",
      inkFaint:dark ? "#8a8272" : "#98917f",
      edge:    dark ? "rgba(179,171,154,0.16)" : "rgba(120,112,96,0.20)",
      accent:  "#a9762a"
    };
  }

  function _rgb(hex) {
    hex = hex.replace("#", "");
    return [parseInt(hex.slice(0, 2), 16), parseInt(hex.slice(2, 4), 16), parseInt(hex.slice(4, 6), 16)];
  }
  function lighten(hex, frac) {           // mix a domain colour toward the surface (paler = thinner page)
    var a = _rgb(hex), b = _rgb(tokens().surface);
    var m = a.map(function (v, i) { return Math.round(v + (b[i] - v) * frac); });
    return "rgb(" + m[0] + "," + m[1] + "," + m[2] + ")";
  }
  function depthFrac(depth) {
    if (!depth || depth < 300) return 0.5;
    if (depth < 800) return 0.32;
    if (depth < 1800) return 0.14;
    return 0.0;
  }
  function depthLabel(d) { return !d || d < 300 ? "thin" : d < 800 ? "medium" : d < 1800 ? "deep" : "very deep"; }
  function titleCase(s) { return (s || "").replace(/\b\w/g, function (m) { return m.toUpperCase(); }); }
  function nodeMatches(n, q) {
    var hay = [(n.title || "")].concat(n.aliases || []).join(" ").toLowerCase();
    return hay.indexOf(q) !== -1;
  }
  function showNodePanel(panel, n) {
    if (n.hub) {
      panel.innerHTML = "<b>" + (n.title || "") + "</b><br>domain hub · " + (n.sources || 0) + " source pages"
        + '<br><a href="' + REPO + "tree/main/corpus/" + n.id + '" target="_blank" rel="noopener">Browse domain →</a>';
    } else {
      panel.innerHTML = "<b>" + (n.title || "") + "</b><br>" + n.domain
        + "<br>" + depthLabel(n.depth) + " · " + (n.depth || 0) + " words · " + (n.degree || 0) + " links"
        + '<br><a href="' + REPO + "blob/main/corpus/" + n.id + '.md" target="_blank" rel="noopener">Open page →</a>';
    }
    panel.style.display = "block";
  }

  function render() {
    var el = document.getElementById("corpus-graph");
    if (!el || typeof vis === "undefined") return;

    var t = tokens();
    if (el.dataset.rendered === "1" && el.dataset.scheme === (t.dark ? "slate" : "default")) return;
    el.innerHTML = "";
    el.dataset.rendered = "1";
    el.dataset.scheme = t.dark ? "slate" : "default";

    fetch("assets/graph-data.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        data.nodes.forEach(function (n) {
          n.domain = n.group;                  // keep the domain for filtering + colour…
          delete n.group;                      // …but strip `group` so vis won't apply its bright default palette
          var base = GROUP_COLORS[n.domain] || t.inkFaint;
          n.shape = "dot";
          n.title = n.label;                   // original label for the panel + search
          if (n.hub) {
            n.value = 46;
            n.label = titleCase(n.domain) + (n.sources ? "  ·  " + n.sources + " sources" : "");
            n.font = { size: 18, face: "Newsreader, Georgia, serif", color: t.ink, strokeWidth: 6, strokeColor: t.surface };
            n.color = { background: base, border: base, highlight: { background: base, border: t.accent }, hover: { background: base, border: t.accent } };
            n.borderWidth = 0;
          } else {
            n.value = Math.max(n.degree || 1, 1);             // SIZE = degree
            var c = lighten(base, depthFrac(n.depth));        // LIGHTNESS = depth
            n.color = { background: c, border: c, highlight: { background: c, border: t.accent }, hover: { background: c, border: t.accent } };
            n.label = undefined;
            if ((n.degree || 0) <= 1) {                       // ORPHAN marker
              n.borderWidth = 1.4; n.shapeProperties = { borderDashes: [2, 2] }; n.color.border = t.inkFaint;
            } else { n.borderWidth = 0; }
          }
        });
        // --- anchored territories: pin hubs on a bridge-affinity ring, seed pages around their hub ---
        function domOf(id) { var i = id.indexOf("/"); return i < 0 ? id : id.slice(0, i); }
        var byId = {}; data.nodes.forEach(function (n) { byId[n.id] = n; });
        var hubDomains = data.nodes.filter(function (n) { return n.hub; }).map(function (n) { return n.id; });

        // domain×domain bridge counts (bridge edges join two page nodes in different domains)
        var bridges = {};
        function pk(a, b) { return a < b ? a + "|" + b : b + "|" + a; }
        data.edges.forEach(function (e) {
          if (!e.bridge) return;
          var a = domOf(e.from), b = domOf(e.to);
          if (a !== b && byId[a] && byId[b]) bridges[pk(a, b)] = (bridges[pk(a, b)] || 0) + 1;
        });
        function pair(a, b) { return bridges[pk(a, b)] || 0; }

        // greedy nearest-neighbour ring order — most-bridged pairs adjacent (short, uncrossed arcs)
        var remaining = hubDomains.slice().sort(function (a, b) {
          var ta = 0, tb = 0; hubDomains.forEach(function (d) { ta += pair(a, d); tb += pair(b, d); });
          return tb - ta;
        });
        var order = remaining.length ? [remaining.shift()] : [];
        while (remaining.length) {
          var last = order[order.length - 1];
          remaining.sort(function (a, b) { return pair(last, b) - pair(last, a); });
          order.push(remaining.shift());
        }

        // pin hubs on the ring (fixed + heavy so nothing drags them into the centre)
        var R = 360;
        order.forEach(function (dom, i) {
          var ang = (i / order.length) * 2 * Math.PI - Math.PI / 2;
          var h = byId[dom];
          h.x = Math.round(Math.cos(ang) * R); h.y = Math.round(Math.sin(ang) * R);
          h.fixed = { x: true, y: true }; h.mass = 8;
        });

        // seed each domain's pages in a small ring around their hub so physics starts them in-territory
        var pagesByDom = {};
        data.nodes.forEach(function (n) { if (!n.hub) (pagesByDom[n.domain] = pagesByDom[n.domain] || []).push(n); });
        Object.keys(pagesByDom).forEach(function (dom) {
          var h = byId[dom]; if (!h) return;
          var ps = pagesByDom[dom];
          ps.forEach(function (n, j) {
            var a = (j / ps.length) * 2 * Math.PI, rr = 36 + (j % 6) * 15;
            n.x = h.x + Math.cos(a) * rr; n.y = h.y + Math.sin(a) * rr;
          });
        });

        var nodes = new vis.DataSet(data.nodes);
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge ? t.accent : t.edge;             // cross-domain BRIDGE edges stand out
          return { from: e.from, to: e.to, color: { color: col, highlight: t.accent, hover: t.accent },
                   width: e.bridge ? 0.9 : 0.5, length: e.bridge ? 520 : 85 };
        }));
        var network = new vis.Network(el, { nodes: nodes, edges: edges }, {
          nodes: { scaling: { min: 6, max: 46 } },
          edges: { smooth: { type: "continuous" }, width: 0.5, selectionWidth: 1 },
          physics: {
            barnesHut: { gravitationalConstant: -2200, centralGravity: 0, springLength: 90, springConstant: 0.03, damping: 0.55, avoidOverlap: 0.4 },
            stabilization: { iterations: 250 }
          },
          interaction: { hover: true, tooltipDelay: 120, hideEdgesOnDrag: true },
          layout: { improvedLayout: false }
        });
        // Freeze the layout once settled: store positions + turn physics off, so filtering never
        // re-runs the (expensive) layout — toggles become instant and nothing flies around.
        network.once("stabilizationIterationsDone", function () {
          network.storePositions();
          network.setOptions({ physics: false });
        });

        // Mark the eight domain hubs with a small centre dot — a subtle bullseye so a hub reads as
        // distinct from the similarly-coloured, similarly-sized sub-nodes around it. Drawn in network
        // coordinates so it scales with zoom and sits dead-centre.
        var hubIds = data.nodes.filter(function (n) { return n.hub; }).map(function (n) { return n.id; });
        network.on("afterDrawing", function (ctx) {
          var pos = network.getPositions(hubIds);
          ctx.save();
          ctx.fillStyle = "rgba(34,29,23,0.88)";
          hubIds.forEach(function (id) {
            var p = pos[id];
            if (!p) return;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI);
            ctx.fill();
          });
          ctx.restore();
        });

        // --- overlay UI (created AFTER vis.Network, which replaces the container's contents) ---
        var panel = document.createElement("div");
        panel.id = "corpus-graph-panel"; panel.style.display = "none"; el.appendChild(panel);
        var controls = document.createElement("div");
        controls.id = "corpus-graph-controls"; el.appendChild(controls);

        var state = { domains: {}, thinOnly: false, orphanOnly: false, cutoff: null, query: "" };

        // ONE batched pass — only nodes whose visibility/opacity actually changes are updated.
        function apply() {
          var upd = [];
          nodes.forEach(function (n) {
            var hide = false, dim = false;
            if (!n.hub) {
              if (state.domains[n.domain] === false) hide = true;
              if (state.thinOnly && (n.depth || 0) >= 300) hide = true;
              if (state.orphanOnly && (n.degree || 0) > 1) hide = true;
              if (state.cutoff && n.created && n.created > state.cutoff) hide = true;
              if (state.query && !nodeMatches(n, state.query)) dim = true;
            }
            var op = dim ? 0.12 : 1;
            if (!!n.hidden !== hide || (n.opacity == null ? 1 : n.opacity) !== op) {
              upd.push({ id: n.id, hidden: hide, opacity: op });
            }
          });
          if (upd.length) nodes.update(upd);
        }

        network.on("click", function (p) {
          if (p.nodes.length) { showNodePanel(panel, nodes.get(p.nodes[0])); }
          else { panel.style.display = "none"; }
        });

        // search (title + alias)
        var search = document.createElement("input");
        search.type = "search"; search.placeholder = "search…"; search.id = "corpus-graph-search";
        search.addEventListener("input", function () { state.query = search.value.trim().toLowerCase(); apply(); });
        controls.appendChild(search);

        // domain chips + thin/orphan toggles
        var domains = Array.from(new Set(data.nodes.filter(function (n) { return !n.hub; })
                                             .map(function (n) { return n.domain; }))).sort();
        domains.forEach(function (dm) {
          state.domains[dm] = true;
          var chip = document.createElement("label"); chip.className = "cg-chip";
          chip.style.setProperty("--chip", GROUP_COLORS[dm] || "#999");
          var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = true;
          cb.addEventListener("change", function () { state.domains[dm] = cb.checked; apply(); });
          chip.appendChild(cb); chip.appendChild(document.createTextNode(dm));
          controls.appendChild(chip);
        });
        [["thinOnly", "thin only"], ["orphanOnly", "orphans"]].forEach(function (pair) {
          var lab = document.createElement("label"); lab.className = "cg-chip cg-chip--flag";
          var cb = document.createElement("input"); cb.type = "checkbox";
          cb.addEventListener("change", function () { state[pair[0]] = cb.checked; apply(); });
          lab.appendChild(cb); lab.appendChild(document.createTextNode(pair[1]));
          controls.appendChild(lab);
        });

        // grown-over-time slider — its own bar, pinned to the bottom of the map
        var dates = data.nodes.filter(function (n) { return n.created; })
                              .map(function (n) { return n.created; }).sort();
        if (dates.length) {
          var row = document.createElement("div"); row.id = "corpus-graph-time";
          var play = document.createElement("button"); play.textContent = "▶"; play.type = "button"; play.title = "play growth";
          var slider = document.createElement("input");
          slider.type = "range"; slider.min = 0; slider.max = dates.length - 1; slider.value = dates.length - 1;
          var lbl = document.createElement("span"); lbl.className = "cg-date"; lbl.textContent = dates[dates.length - 1];
          slider.addEventListener("input", function () {
            var v = +slider.value;
            state.cutoff = v >= dates.length - 1 ? null : dates[v];
            lbl.textContent = dates[v]; apply();
          });
          var timer = null;
          play.addEventListener("click", function () {
            if (timer) { clearInterval(timer); timer = null; play.textContent = "▶"; return; }
            play.textContent = "❙❙"; if (+slider.value >= +slider.max) slider.value = 0;
            timer = setInterval(function () {
              if (+slider.value >= +slider.max) { clearInterval(timer); timer = null; play.textContent = "▶"; return; }
              slider.value = +slider.value + 1; slider.dispatchEvent(new Event("input"));
            }, 140);
          });
          row.appendChild(play); row.appendChild(slider); row.appendChild(lbl);
          el.appendChild(row);
        }
      })
      .catch(function () {});
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(render);
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
})();
