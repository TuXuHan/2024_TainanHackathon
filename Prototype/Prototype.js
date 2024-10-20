const slider = document.getElementById("distanceslider");
const output = document.getElementById("distancevalue");

slider.oninput = function() {
    output.innerText = `${this.value} km`;
};

document.getElementById("searchbtn").onclick = async () => {
    
    const searchword = document.getElementById("searchword").value;
    const searchdistance= slider.value;

    console.log('searchword: ', searchword);
    console.log('searchdistance: ', searchdistance);

    const response = await fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ searchword, searchdistance })
    });

    if (response.ok) {
        const data = await response.text();
        document.getElementById("result").innerHTML = data;
    } else {
        const errorData = await response.json();
        console.error("Error details:", errorData);
        document.getElementById("result").innerText = "Error occurred! " + JSON.stringify(errorData);
    }
};

