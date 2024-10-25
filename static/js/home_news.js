const newsData = [
    {
        title: "{{ news_list.0.title }}",
        description: "{{ news_list.0.short_description }}",
        image: "{{ news_list.0.image.url }}"
    },
    {
        title: "{{ news_list.1.title }}",
        description: "{{ news_list.1.short_description }}",
        image: "{{ news_list.1.image.url }}"
    },
    {
        title: "{{ news_list.2.title }}",
        description: "{{ news_list.2.short_description }}",
        image: "{{ news_list.2.image.url }}"
    }
];

function selectNews(index) {
    const selectedThumbnail = document.querySelectorAll('.thumbnail')[index];
    const image = selectedThumbnail.getAttribute('data-image');
    const title = selectedThumbnail.getAttribute('data-title');
    const id = selectedThumbnail.getAttribute('data-id');
    const description = selectedThumbnail.getAttribute('data-description');

    const newid = "/news_detailed/" + id + "/";

    console.log(newid);

    document.getElementById('main-news-image').src = image;
    document.getElementById('news-title').textContent = title;
    document.getElementById('news-description').textContent = description;
    document.getElementById('news-id').href = newid;

    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumbnail, idx) => {
        if (idx === index) {
            thumbnail.classList.add('active');
        } else {
            thumbnail.classList.remove('active');
        }
    });
}



function onStart()
{
    selectNews(0);

}