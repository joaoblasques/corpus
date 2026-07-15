/* Corpus knowledge graph — "Archive" theme + diagnostic encodings + interactivity.
   Rendering is truthful: node SIZE = connection count (degree), LIGHTNESS = page depth
   (word count), hub labels carry source counts, cross-domain "bridge" edges are accented,
   and orphans (degree 1) get a dashed ring. On top of that: click a node for a summary +
   link to its source, search by title/alias, filter by domain/depth/orphan, and a
   grown-over-time slider (by each page's `created` date). Data is regenerated from the real
   corpus at every build (hooks/corpus_graph.py) — only titles + structure, never page text. */
(function () {
  var REPO = "https://github.com/joaoblasques/corpus/";

  var GROUP_COLORS = {
    "ai-engineering":       "#5a7a5a",
    "data-engineering":     "#c08a3a",
    "mlops":                "#b06a34",
    "software-engineering": "#6a7d9c",
    "ai-business":          "#a89228",
    "blockchain":           "#8a7aa8",
    "productivity":         "#7a9a5a",
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

  // --- diagnostic helpers -------------------------------------------------
  function _rgb(hex) {
    hex = hex.replace("#", "");
    return [parseInt(hex.slice(0, 2), 16), parseInt(hex.slice(2, 4), 16), parseInt(hex.slice(4, 6), 16)];
  }
  function lighten(hex, frac) {        // mix a domain color toward the surface (paler = thinner page)
    var a = _rgb(hex), b = _rgb(tokens().surface);
    var m = a.map(function (v, i) { return Math.round(v + (b[i] - v) * frac); });
    return "rgb(" + m[0] + "," + m[1] + "," + m[2] + ")";
  }
  function depthFrac(depth) {          // thin pages get more lightening
    if (!depth || depth < 300) return 0.55;
    if (depth < 800) return 0.35;
    if (depth < 1800) return 0.15;
    return 0.0;
  }
  function depthLabel(d) { return !d || d < 300 ? "thin" : d < 800 ? "medium" : d < 1800 ? "deep" : "very deep"; }
  function titleCase(s) { return (s || "").replace(/\b\w/g, function (m) { return m.toUpperCase(); }); }
  function nodeMatches(n, q) {
    if (!q) return true;
    var hay = [(n.title || "")].concat(n.aliases || []).join(" ").toLowerCase();
    return hay.indexOf(q.toLowerCase()) !== -1;
  }
  function showNodePanel(panel, n) {
    if (n.hub) {
      panel.innerHTML = "<b>" + (n.title || "") + "</b><br>domain hub<br>" + (n.sources || 0) + " source pages"
        + '<br><a href="' + REPO + "tree/main/corpus/" + n.id + '" target="_blank" rel="noopener">Browse domain →</a>';
    } else {
      panel.innerHTML = "<b>" + (n.title || "") + "</b><br>" + n.group
        + "<br>depth: " + depthLabel(n.depth) + " (" + (n.depth || 0) + " words)"
        + "<br>connections: " + (n.degree || 0)
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
          var base = GROUP_COLORS[n.group] || t.inkFaint;
          n.shape = "dot";
          n.title = n.label;                                  // keep the original label for panel + search
          if (n.hub) {
            n.value = 46;
            n.label = titleCase(n.label) + (n.sources ? "  ·  " + n.sources + " sources" : "");
            n.font = { size: 19, face: "Newsreader, Georgia, serif", color: t.ink, strokeWidth: 6, strokeColor: t.surface };
            n.color = { background: base, border: base, highlight: { background: base, border: t.accent }, hover: { background: base, border: t.accent } };
            n.borderWidth = 0;
          } else {
            n.value = Math.max(n.degree || 1, 1);             // SIZE = degree
            var shaded = lighten(base, depthFrac(n.depth));   // LIGHTNESS = depth
            n.color = { background: shaded, border: shaded, highlight: { background: shaded, border: t.accent }, hover: { background: shaded, border: t.accent } };
            n.label = undefined;
            if ((n.degree || 0) <= 1) {                       // ORPHAN marker
              n.borderWidth = 1.5;
              n.shapeProperties = { borderDashes: [2, 2] };
              n.color.border = t.inkFaint;
            } else {
              n.borderWidth = 0;
            }
          }
        });
        var nodes = new vis.DataSet(data.nodes);
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge ? t.accent : t.edge;             // cross-domain BRIDGE edges stand out
          return { from: e.from, to: e.to,
                   color: { color: col, highlight: t.accent, hover: t.accent },
                   width: e.bridge ? 0.9 : 0.5 };
        }));
        var network = new vis.Network(el, { nodes: nodes, edges: edges }, {
          nodes: { scaling: { min: 6, max: 46 } },
          edges: { smooth: { type: "continuous" }, width: 0.5, selectionWidth: 1 },
          physics: {
            barnesHut: { gravitationalConstant: -3600, springLength: 155, springConstant: 0.02, damping: 0.5, avoidOverlap: 0.3 },
            stabilization: { iterations: 200 }
          },
          interaction: { hover: true, tooltipDelay: 120, hideEdgesOnDrag: true },
          layout: { improvedLayout: false }
        });
        network.once("stabilizationIterationsDone", function () { network.setOptions({ physics: false }); });

        // Overlay containers — created AFTER vis.Network (which replaces the container's contents,
        // so anything appended before init would be wiped). Positioned absolutely over the canvas.
        var panel = document.createElement("div");
        panel.id = "corpus-graph-panel"; panel.style.display = "none"; el.appendChild(panel);
        var controls = document.createElement("div");
        controls.id = "corpus-graph-controls"; el.appendChild(controls);

        // --- filters + time compose through one visibility pass; hubs never hidden ---
        var state = { domains: {}, thinOnly: false, orphanOnly: false, cutoff: null };
        function applyVisibility() {
          nodes.forEach(function (n) {
            if (n.hub) { nodes.update({ id: n.id, hidden: false }); return; }
            var show = state.domains[n.group] !== false;
            if (state.thinOnly && (n.depth || 0) >= 300) show = false;
            if (state.orphanOnly && (n.degree || 0) > 1) show = false;
            if (state.cutoff && n.created && n.created > state.cutoff) show = false;
            nodes.update({ id: n.id, hidden: !show });
          });
        }

        // click → summary panel
        network.on("click", function (params) {
          if (params.nodes.length) { showNodePanel(panel, nodes.get(params.nodes[0])); }
          else { panel.style.display = "none"; }
        });

        // search box (dims non-matches by title/alias)
        var searchBox = document.createElement("input");
        searchBox.type = "search"; searchBox.placeholder = "search…"; searchBox.id = "corpus-graph-search";
        controls.appendChild(searchBox);
        searchBox.addEventListener("input", function () {
          var q = searchBox.value.trim();
          nodes.forEach(function (n) {
            var on = n.hub || nodeMatches(n, q);
            nodes.update({ id: n.id, opacity: q ? (on ? 1 : 0.12) : 1 });
          });
        });

        // domain chips + thin/orphan toggles
        var domains = Array.from(new Set(data.nodes.filter(function (n) { return !n.hub; })
                                             .map(function (n) { return n.group; }))).sort();
        domains.forEach(function (dm) {
          state.domains[dm] = true;
          var chip = document.createElement("label"); chip.className = "cg-chip";
          chip.style.borderColor = GROUP_COLORS[dm] || "#999";
          var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = true;
          cb.addEventListener("change", function () { state.domains[dm] = cb.checked; applyVisibility(); });
          chip.appendChild(cb); chip.appendChild(document.createTextNode(dm));
          controls.appendChild(chip);
        });
        [["thinOnly", "thin only"], ["orphanOnly", "orphans"]].forEach(function (pair) {
          var lab = document.createElement("label"); lab.className = "cg-chip";
          var cb = document.createElement("input"); cb.type = "checkbox";
          cb.addEventListener("change", function () { state[pair[0]] = cb.checked; applyVisibility(); });
          lab.appendChild(cb); lab.appendChild(document.createTextNode(pair[1]));
          controls.appendChild(lab);
        });

        // grown-over-time slider (by page `created` date)
        var dates = data.nodes.filter(function (n) { return n.created; })
                              .map(function (n) { return n.created; }).sort();
        if (dates.length) {
          var row = document.createElement("div"); row.id = "corpus-graph-time";
          var slider = document.createElement("input");
          slider.type = "range"; slider.min = 0; slider.max = dates.length - 1; slider.value = dates.length - 1;
          var lbl = document.createElement("span"); lbl.textContent = dates[dates.length - 1];
          var play = document.createElement("button"); play.textContent = "▶"; play.type = "button";
          slider.addEventListener("input", function () {
            state.cutoff = dates[+slider.value]; lbl.textContent = state.cutoff; applyVisibility();
          });
          var timer = null;
          play.addEventListener("click", function () {
            if (timer) { clearInterval(timer); timer = null; play.textContent = "▶"; return; }
            play.textContent = "⏸"; if (+slider.value >= +slider.max) { slider.value = 0; }
            timer = setInterval(function () {
              if (+slider.value >= +slider.max) { clearInterval(timer); timer = null; play.textContent = "▶"; return; }
              slider.value = +slider.value + 1; slider.dispatchEvent(new Event("input"));
            }, 180);
          });
          row.appendChild(play); row.appendChild(slider); row.appendChild(lbl);
          controls.appendChild(row);
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
