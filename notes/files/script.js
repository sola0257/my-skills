function zoomImage(img) {
    if (img.classList.contains('zoomed')) {
        img.classList.remove('zoomed');
        document.querySelector('.overlay').remove();
    } else {
        var overlay = document.createElement('div');
        overlay.classList.add('overlay');

        var zoomedImg = img.cloneNode(true);
        zoomedImg.removeAttribute('width');
        zoomedImg.removeAttribute('height');
        zoomedImg.classList.add('zoomed');

        overlay.appendChild(zoomedImg);

        overlay.onclick = function (e) {
            if (e.target === overlay) {
                overlay.remove();
            }
        };

        document.body.appendChild(overlay);
    }
}


function initIndexPage() {
    const notesList = document.getElementById('notesList');
    const dateFilter = document.getElementById('dateFilter');
    const tagFilter = document.getElementById('tagFilter');
    const filterButton = document.getElementById('filterButton');

    if (!notesList || !dateFilter || !tagFilter || !filterButton) {
        return;
    }

    const notes = notesList.querySelectorAll('tbody tr');

    const dates = new Set();
    const tags = new Set();

    function extractYearMonth(dateStr) {
        const [datePart] = dateStr.split(' ');
        const [year, month] = datePart.split('-');
        return `20${year}-${month}`;
    }

    Array.from(notes).forEach(note => {
        const dateStr = note.dataset.dateStr;
        const yearMonth = extractYearMonth(dateStr);
        const tagString = note.dataset.tags;

        if (yearMonth) {
            dates.add(yearMonth);
        }

        if (tagString) {
            tagString.split(',').forEach(tag => {
                if (tag.trim()) {
                    tags.add(tag.trim());
                }
            });
        }
    });

    const sortedDates = Array.from(dates).sort((a, b) => new Date(b) - new Date(a));

    sortedDates.forEach(date => {
        const option = document.createElement('option');
        option.value = date;
        option.textContent = date;
        dateFilter.appendChild(option);
    });

    const sortedTags = Array.from(tags).sort((a, b) => {
        const isPunctuation = (str) => /^[^\w\s\u4e00-\u9fa5]/.test(str);
        const isLetter = (str) => /^[a-zA-Z]/.test(str);

        if (isPunctuation(a) && !isPunctuation(b)) return -1;
        if (!isPunctuation(a) && isPunctuation(b)) return 1;
        if (isPunctuation(a) && isPunctuation(b)) return a.localeCompare(b);

        if (isLetter(a) && !isLetter(b)) return -1;
        if (!isLetter(a) && isLetter(b)) return 1;

        return a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'});
    });

    sortedTags.forEach(tag => {
        const option = document.createElement('option');
        option.value = tag;
        option.textContent = tag;
        tagFilter.appendChild(option);
    });

    function applyFilter() {
        const selectedDate = dateFilter.value;
        const selectedTag = tagFilter.value;

        Array.from(notes).forEach(note => {
            const noteDate = extractYearMonth(note.dataset.dateStr);
            const noteTags = (note.dataset.tags || '').split(',').map(tag => tag.trim());

            const dateMatch = !selectedDate || noteDate === selectedDate;
            const tagMatch = !selectedTag || noteTags.includes(selectedTag);

            note.style.display = dateMatch && tagMatch ? '' : 'none';

            const link = note.querySelector('a');
            if (link) {
                const originalHref = link.getAttribute('href');
                let newHref = originalHref.split('?')[0];
                const params = [];
                if (selectedDate) {
                    params.push(`date=${encodeURIComponent(selectedDate)}`);
                }
                if (selectedTag) {
                    params.push(`tag=${encodeURIComponent(selectedTag)}`);
                }
                if (params.length > 0) {
                    newHref += '?' + params.join('&');
                }
                link.setAttribute('href', newHref);
            }
        });
    }

    filterButton.addEventListener('click', applyFilter);

    const urlParams = new URLSearchParams(window.location.search);
    const dateParam = urlParams.get('date');
    const tagParam = urlParams.get('tag');

    if (dateParam) {
        dateFilter.value = dateParam;
    }
    if (tagParam) {
        tagFilter.value = tagParam;
    }
    if (dateParam || tagParam) {
        applyFilter();
    }

    const dateHeader = document.getElementById('dateHeader');
    const sortIcon = dateHeader.querySelector('.sort-icon');
    let isAscending = false;

    sortNotes();

    dateHeader.addEventListener('click', function () {
        isAscending = !isAscending;
        sortNotes();
    });

    function sortNotes() {
        const tbody = document.querySelector('#notesList tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const parseDate = (dateStr) => {
                const [datePart, timePart] = dateStr.split(' ');
                const [year, month, day] = datePart.split('-').map(Number);
                const [hour, minute] = timePart.split(':').map(Number);
                return new Date(2000 + year, month - 1, day, hour, minute);
            };

            const dateA = parseDate(a.getAttribute('data-date-str'));
            const dateB = parseDate(b.getAttribute('data-date-str'));

            return isAscending ? dateA - dateB : dateB - dateA;
        });

        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));

        sortIcon.textContent = isAscending ? '\u25B3' : '\u25BD';
    }
}

function initDetailPage() {
    const backLink = document.getElementById('backLink');
    if (backLink) {
        const urlParams = new URLSearchParams(window.location.search);
        const dateFilter = urlParams.get('date');
        const tagFilter = urlParams.get('tag');

        let backUrl = '../index.html';
        const params = [];

        if (urlParams.has('date')) {
            params.push(`date=${encodeURIComponent(dateFilter)}`);
        }

        if (urlParams.has('tag')) {
            params.push(`tag=${encodeURIComponent(tagFilter)}`);
        }

        if (params.length > 0) {
            backUrl += '?' + params.join('&');
        }

        backLink.href = backUrl;
    }
}
