const popoverList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
popoverList.map((el) => {
    let opts = {
        animation: false,
    }
    if (el.hasAttribute('data-bs-content-id')) {
        const contentSource = document.getElementById(el.getAttribute('data-bs-content-id'))
        opts.title = contentSource.getAttribute('data-bs-title');
        opts.content = contentSource.innerHTML;
        opts.customClass = 'custom-popover';
        opts.html = true;
    }
    new bootstrap.Popover(el, opts);
})
