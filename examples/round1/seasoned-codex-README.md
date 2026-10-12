<h1>Tools for safer Postgres operations.</h1>

<p>I'm Ingrid — staff-level engineer, previously SRE.</p>

<h2>Before production. During an incident.</h2>

<h3><a href="https://github.com/ingridh-demo/migra-lint"><samp>migra-lint</samp></a> · Check the migration</h3>

<p>Catch locks, table rewrites and blocked writes before deployment. Static analysis with safer alternatives, available as a CLI, Go library and GitHub Action.</p>

<pre><code>migra-lint check migrations/*.sql</code></pre>

<h3><a href="https://github.com/ingridh-demo/pgwhen"><samp>pgwhen</samp></a> · Inspect the past</h3>

<p>Query a read-only Postgres endpoint at a chosen timestamp. Restores WAL archives into ephemeral instances for incident forensics; works with pgBackRest and WAL-G.</p>

<p><a href="https://github.com/ingridh-demo/pg-lockviz"><samp>pg-lockviz</samp></a> — See who blocks whom, from <code>pg_locks</code> snapshots.<br>
<a href="https://github.com/ingridh-demo/tracehound"><samp>tracehound</samp></a> — Break down Postgres query latency with eBPF, without application changes. Experimental; Linux ≥ 5.15.</p>

<h2>Conference talks</h2>

<p>I speak about Postgres locks, tracing and incident forensics.</p>

<ul>
<li>Locks you didn't know you took — PGConf.EU 2025</li>
<li>Tracing the last millisecond — P2D2 2026</li>
<li>Time travel for operators — FOSDEM 2024</li>
</ul>

<p><a href="https://github.com/ingridh-demo/talks">Slides, notes &amp; available recordings →</a></p>

<hr>

<p><a href="https://ingrid.dev">Blog</a> · <a href="https://hachyderm.io/@ingridh">Mastodon</a> · <a href="https://www.linkedin.com/in/ingrid-halvorsen-example">LinkedIn</a></p>
