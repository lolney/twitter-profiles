path = location.path.split('/');
username = path[2];

$.get("http://localhost:5000/profile/" + username + "/frequencies", function(interests, status){

var chart = bb.generate({
    data: {
        columns: interests,
        type : 'donut',
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    },
    donut: {
        title: "Interests"
    }
});

setTimeout(function () {
    chart.load({
        columns: interests
    });
}, 1);

/*
setTimeout(function () {
    chart.unload({
        ids: 'data1'
    });
    chart.unload({
        ids: 'data2'
    });
}, 2500);
*/
    }                                                                         
    );


