<style>
  /* Widen only the Publications page on desktop. */
  @media (min-width: 992px) {
    .publications-wide {
      width: min(1240px, calc(100vw - 64px));
      max-width: none;
      position: relative;
      left: 50%;
      transform: translateX(-50%);
    }

    /*
     * Keep the thumbnail at approximately its current desktop size.
     * The extra width goes to the publication information column.
     */
    .publications-wide .pub-custom-media {
      flex: 0 0 410px;
      width: 410px;
      max-width: 410px;
    }

    .publications-wide .pub-custom-info {
      flex: 1 1 auto;
      min-width: 0;
    }
  }

  /* On smaller screens, keep the normal responsive behavior. */
  @media (max-width: 991.98px) {
    .publications-wide {
      width: 100%;
      max-width: 100%;
      position: static;
      left: auto;
      transform: none;
    }
  }
</style>

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications publications-wide">

{% bibliography %}

</div>
