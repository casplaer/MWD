function selectNews(index) {
    const selectedThumbnail = document.querySelectorAll('.news-item')[index-1];
    const image = selectedThumbnail.getAttribute('data-image');
    const title = selectedThumbnail.getAttribute('data-title');
    // const id = selectedThumbnail.getAttribute('data-id');
    const description = selectedThumbnail.getAttribute('data-description');

    const newid = "/news_detailed/" + index + "/";

    console.log(title);

    document.getElementById('details-image').src = image;
    document.getElementById('details-link').href = newid;
    document.getElementById('details-description').textContent = description;
    document.getElementById('details-title').textContent = title;

    // const thumbnails = document.querySelectorAll('.thumbnail');
    // thumbnails.forEach((thumbnail, idx) => {
    //     if (idx === index) {
    //         thumbnail.classList.add('active');
    //     } else {
    //         thumbnail.classList.remove('active');
    //     }
    // });
}
