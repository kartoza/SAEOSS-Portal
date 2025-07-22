$(document).ready(function () {
    const ITEMS_PER_PAGE = 2;
    window.allThematicItems = {}; // Global store for items per group

    $.ajax({
        url: '/thematic/all/',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            const results = response.results;
            let allHtml = '';

            for (const groupName in results) {
                const title = groupName.charAt(0).toUpperCase() + groupName.slice(1);
                const items = results[groupName];

                const groupId = `group_${groupName.replace(/\s+/g, '_')}`;
                const totalPages = Math.ceil(items.length / ITEMS_PER_PAGE);

                window.allThematicItems[groupId] = items;

                let groupHtml = `<div class="thematic-group" id="${groupId}">
                    <h3 class="thematic-group-title text-muted">${title}</h3>
                    <div class="row thematic-items" data-group="${groupId}" data-page="1">`;

                groupHtml += renderThematicItems(items, 1, ITEMS_PER_PAGE);

                groupHtml += `</div>
                    <nav class="mt-2">
                        <ul class="pagination justify-content-center">`;

                for (let page = 1; page <= totalPages; page++) {
                    groupHtml += `
                        <li class="page-item ${page === 1 ? 'active' : ''}">
                            <a class="page-link" href="#" data-group="${groupId}" data-page="${page}">${page}</a>
                        </li>`;
                }

                groupHtml += `</ul>
                    </nav>
                </div><br>`;

                allHtml += groupHtml;
            }

            $('#thematic_groups').html(allHtml);
        },
        error: function (xhr, status, error) {
            console.error('Error fetching data:', error);
        }
    });

    function renderThematicItems(items, currentPage, itemsPerPage) {
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedItems = items.slice(start, end);

        let html = '';
        for (const ds of paginatedItems) {
            const notes = ds.notes ? `<p>${ds.notes}</p>` : '';
            var imageUrl = ds.image_url || '/images/org.png';
            html += `<div class="col-md-6">
                <div class="thematic-item-card mb-4">
                    <div class="thematic-item-card-body">
                        <div class="thematic-item-image-parent">
                            <img src="${imageUrl}" alt="${ds.title}" class="thematic-item-image">
                        </div>
                        <h5 class="thematic-item-card-title text-muted">${ds.title}</h5>
                        <div class="thematic-item-card-text text-muted">${notes}</div>
                        <a href="/dataset/${ds.name}" class="btn btn-primary">View Dataset</a>
                    </div>
                </div>
            </div>`;
        }

        return html;
    }

    // Handle pagination click
    $(document).on('click', '.pagination a.page-link', function (e) {
        e.preventDefault();

        const groupId = $(this).data('group');
        const page = parseInt($(this).data('page'));
        const items = window.allThematicItems[groupId] || [];

        const groupContainer = $(`#${groupId}`);
        groupContainer.find('.thematic-items')
            .html(renderThematicItems(items, page, ITEMS_PER_PAGE))
            .attr('data-page', page);

        // Update active page styling
        groupContainer.find('.pagination li').removeClass('active');
        $(this).parent().addClass('active');
    });
});