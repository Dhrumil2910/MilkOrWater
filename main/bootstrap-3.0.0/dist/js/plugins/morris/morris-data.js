// Morris.js Charts sample data for SB Admin template

$(function() {

    // Area Chart
    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2010 Q1',
            Aegion: 26.66,
            Adobe: null,
            Allegion: 26.47
        }, {
            period: '2010 Q2',
            Aegion: 27.78,
            Adobe: 22.94,
            Allegion: 24.41
        }, {
            period: '2010 Q3',
            Aegion: 49.12,
            Adobe: 19.69,
            Allegion: 25.01
        }, {
            period: '2010 Q4',
            Aegion: 37.67,
            Adobe: 35.97,
            Allegion: 56.89
        }, {
            period: '2011 Q1',
            Aegion: 68.10,
            Adobe: 19.14,
            Allegion: 22.93
        }, {
            period: '2011 Q2',
            Aegion: 56.70,
            Adobe: 42.93,
            Allegion: 18.81
        }, {
            period: '2011 Q3',
            Aegion: 48.20,
            Adobe: 37.95,
            Allegion: 15.88
        }, {
            period: '2011 Q4',
            Aegion: 15.073,
            Adobe: 59.67,
            Allegion: 51.75
        }, {
            period: '2012 Q1',
            Aegion: 10.687,
            Adobe: 44.60,
            Allegion: 20.28
        }, {
            period: '2012 Q2',
            Aegion: 84.32,
            Adobe: 57.13,
            Allegion: 17.91
        }],
        xkey: 'period',
        ykeys: ['Aegion', 'Adobe', 'Allegion'],
        labels: ['Aegion', 'Adobe Systems', 'Allegion'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });

    // Donut Chart
    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Health Care",
            value: 3
        }, {
            label: "Consumer Services",
            value: 5
        }, {
            label: "Technology",
            value: 5
        }],
        resize: true
    });

    // Line Chart
    Morris.Line({
        // ID of the element in which to draw the chart.
        element: 'morris-line-chart',
        // Chart data records -- each entry in this array corresponds to a point on
        // the chart.
        data: [{
            d: '2012-10-01',
            Volume: 802
        }, {
            d: '2012-10-02',
            Volume: 783
        }, {
            d: '2012-10-03',
            Volume: 820
        }, {
            d: '2012-10-04',
            Volume: 839
        }, {
            d: '2012-10-05',
            Volume: 792
        }, {
            d: '2012-10-06',
            Volume: 859
        }, {
            d: '2012-10-07',
            Volume: 790
        }, {
            d: '2012-10-08',
            Volume: 1680
        }, {
            d: '2012-10-09',
            Volume: 1592
        }, {
            d: '2012-10-10',
            Volume: 1420
        }, {
            d: '2012-10-11',
            Volume: 882
        }, {
            d: '2012-10-12',
            Volume: 889
        }, {
            d: '2012-10-13',
            Volume: 819
        }, {
            d: '2012-10-14',
            Volume: 849
        }, {
            d: '2012-10-15',
            Volume: 870
        }, {
            d: '2012-10-16',
            Volume: 1063
        }, {
            d: '2012-10-17',
            Volume: 1192
        }, {
            d: '2012-10-18',
            Volume: 1224
        }, {
            d: '2012-10-19',
            Volume: 1329
        }, {
            d: '2012-10-20',
            Volume: 1329
        }, {
            d: '2012-10-21',
            Volume: 1239
        }, {
            d: '2012-10-22',
            Volume: 1190
        }, {
            d: '2012-10-23',
            Volume: 1312
        }, {
            d: '2012-10-24',
            Volume: 1293
        }, {
            d: '2012-10-25',
            Volume: 1283
        }, {
            d: '2012-10-26',
            Volume: 1248
        }, {
            d: '2012-10-27',
            Volume: 1323
        }, {
            d: '2012-10-28',
            Volume: 1390
        }, {
            d: '2012-10-29',
            Volume: 1420
        }, {
            d: '2012-10-30',
            Volume: 1529
        }, {
            d: '2012-10-31',
            Volume: 1892
        }, ],
        // The name of the data record attribute that contains x-Volumes.
        xkey: 'd',
        // A list of names of data record attributes that contain y-Volumes.
        ykeys: ['Volume'],
        // Labels for the ykeys -- will be displayed when you hover over the
        // chart.
        labels: ['Volume( x10^4)'],
        // Disables line smoothing
        smooth: false,
        resize: true
    });

 // Bar Chart
    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            company: 'ECYT',
            PriceT: 15
        }, {
            company: 'IRWD',
            PriceT: 16
        }, {
            company: 'ADBE',
            PriceT: 74
        }, {
            company: 'ALLE',
            PriceT: 60
        }, {
            company: 'GPS',
            PriceT: 60
        }, {
            company: 'GRMN',
            PriceT: 52
        }],
        xkey: 'company',
        ykeys: ['PriceT'],
        labels: ['Price Targets'],
        barRatio: 0.4,
        xLabelAngle: 35, 
        hideHover: 'auto',
        resize: true
    }); 


});
