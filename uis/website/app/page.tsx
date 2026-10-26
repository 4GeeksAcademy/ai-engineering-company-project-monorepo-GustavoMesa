const highlights = [
  {
    number: "01",
    title: "El fuego como origen",
    text: "Una cocina que celebra el sabor de la brasa y el cuidado de cada preparación.",
  },
  {
    number: "02",
    title: "Hecho para compartir",
    text: "Una mesa abierta para encontrarnos, conversar y disfrutar sin afán.",
  },
  {
    number: "03",
    title: "Un mismo espíritu",
    text: "Nacimos en Medellín y llevamos nuestra manera de reunirnos a nuevos lugares.",
  },
];

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="brand" href="#inicio" aria-label="Brasaland, inicio">
          <span className="brand-mark" aria-hidden="true">
            B
          </span>
          <span>BRASALAND</span>
        </a>
        <nav aria-label="Navegación principal">
          <a href="#historia">Nuestra historia</a>
          <a href="#experiencia">La experiencia</a>
          <a className="nav-cta" href="#visitanos">
            Ven a compartir <span aria-hidden="true">↗</span>
          </a>
        </nav>
      </header>

      <section className="hero" id="inicio">
        <div className="hero-texture" aria-hidden="true" />
        <div className="hero-copy">
          <p className="eyebrow"><span /> COCINA A LA BRASA · DESDE 2008</p>
          <h1>El fuego nos<br />reúne.</h1>
          <p className="hero-intro">
            Hay sabores que empiezan en la brasa y terminan alrededor de una
            buena mesa. Esta es nuestra forma de compartir.
          </p>
          <a className="button button-light" href="#historia">
            Conoce Brasaland <span aria-hidden="true">↓</span>
          </a>
        </div>
        <div className="hero-art" aria-label="Ilustración abstracta de fuego y brasa">
          <div className="sun" />
          <div className="ember ember-one" />
          <div className="ember ember-two" />
          <div className="flame flame-back" />
          <div className="flame flame-front" />
          <div className="grill-line grill-one" />
          <div className="grill-line grill-two" />
          <span className="art-caption">MEDELLÍN · FLORIDA</span>
        </div>
        <div className="hero-bottom">
          <span>UNA HISTORIA QUE SIGUE ENCENDIDA</span>
          <span>03° 27&apos; N &nbsp; · &nbsp; 76° 32&apos; W</span>
        </div>
      </section>

      <section className="intro-section" id="historia">
        <div className="section-label">
          <span>01</span>
          <span>NUESTRA HISTORIA</span>
        </div>
        <div className="intro-copy">
          <p className="kicker">DE MEDELLÍN PARA LA MESA</p>
          <h2>
            Empezamos con una brasa.
            <br />
            <span>Y una mesa para todos.</span>
          </h2>
          <p className="body-copy">
            Desde 2008, Brasaland crece alrededor de una idea sencilla: la
            comida sabe mejor cuando se comparte. Nuestra historia nació en
            Medellín y hoy conecta personas a ambos lados de la mesa.
          </p>
          <a className="text-link" href="#experiencia">
            Así entendemos la hospitalidad <span aria-hidden="true">↗</span>
          </a>
        </div>
        <div className="year-stamp" aria-label="Fundado en 2008">
          <span>DESDE</span>
          <strong>2008</strong>
          <span>MEDELLÍN, COLOMBIA</span>
        </div>
      </section>

      <section className="experience-section" id="experiencia">
        <div className="experience-heading">
          <div className="section-label section-label-light">
            <span>02</span>
            <span>LO QUE NOS MUEVE</span>
          </div>
          <h2>Más que una comida.<br /><em>Un momento para recordar.</em></h2>
        </div>
        <div className="highlight-grid">
          {highlights.map((item) => (
            <article className="highlight-card" key={item.number}>
              <span className="highlight-number">{item.number}</span>
              <div className="highlight-rule" />
              <h3>{item.title}</h3>
              <p>{item.text}</p>
              <span className="highlight-arrow" aria-hidden="true">↗</span>
            </article>
          ))}
        </div>
      </section>

      <section className="visit-section" id="visitanos">
        <div className="visit-orbit visit-orbit-one" aria-hidden="true" />
        <div className="visit-orbit visit-orbit-two" aria-hidden="true" />
        <p className="kicker">LA MESA ESTÁ SERVIDA</p>
        <h2>Nos vemos<br /><span>alrededor del fuego.</span></h2>
        <p className="visit-copy">
          Estamos en Colombia y Florida. Busca tu sede Brasaland y ven a
          compartir.
        </p>
        <div className="city-tags">
          <span>Medellín</span>
          <span>Florida</span>
        </div>
      </section>

      <footer className="site-footer">
        <a className="brand footer-brand" href="#inicio">
          <span className="brand-mark" aria-hidden="true">B</span>
          <span>BRASALAND</span>
        </a>
        <span>Fuego, sabor y encuentros.</span>
        <span>© 2026 Brasaland</span>
      </footer>
    </main>
  );
}
