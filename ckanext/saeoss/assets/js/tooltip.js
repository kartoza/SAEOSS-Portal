$( document ).ready(function() {
    const setTooltip = () => {
        $('#dataset-map').tooltip({
            title: 'Filter by geometry. Can also show boundaries from national to local municipalities.'
        });
        $('#temporal-search').tooltip({
            title: 'Filter by start date, end date, or both.'
        });
        $('#headOrganizations').tooltip({
            title: 'Filter by Organization (SAEOSS collection where metadata belongs to).'
        });
        $('#headHarvestsource').tooltip({
            title: 'Filter by Harvest source. Only applicable for metadata obtained via harvest.'
        });
        $('#headFeaturedMetadatarecords').tooltip({
            title: 'Show only featured metadata (metadata shown on homepage).'
        });
        $('#headTags').tooltip({
            title: 'Filter by tags.'
        });
        $('#headGroups').tooltip({
            title: 'Filter by groups.'
        });
    }
    setTimeout(setTooltip, 2000)
});