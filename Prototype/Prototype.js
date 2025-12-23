import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

const supabaseUrl = 'https://ocrstydcjvxqbhjmxwnb.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jcnN0eWRjanZ4cWJoam14d25iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAxOTI3MTAsImV4cCI6MjA0NTc2ODcxMH0.ZupOGBcMk73nP8IMxbAUqzTx-weHM9RxmU48v-Tzpaw'
const supabase = createClient(supabaseUrl, supabaseKey)

document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll('.star');
    let selectedRating = 0;

    let addToFolderButton;
    let inputField;

    const slider = document.getElementById("distanceslider");
    const output = document.getElementById("distancevalue");

    const numslider = document.getElementById("numslider");
    const numoutput = document.getElementById("numvalue");

    const reviewslider = document.getElementById("reviewslider");
    const reviewoutput = document.getElementById("reviewvalue");

//    updateDistanceValue(slider.value);
    updateNumValue(numslider.value);
//    updateReviewValue(reviewslider.value);

//    slider.oninput = function () {
//        updateDistanceValue(this.value);
//    };

    numslider.oninput = function () {
        updateNumValue(this.value);
    };

//    reviewslider.oninput = function () {
//        updateReviewValue(this.value);
//    };

    stars.forEach((star, index) => {
        star.addEventListener('mouseover', () => {
            highlightStars(index);
        });

        star.addEventListener('mouseout', () => {
            highlightStars(selectedRating - 1); 
        });

        star.addEventListener('click', () => {
            selectedRating = index + 1; 
            highlightStars(index);
            console.log('選擇的星等:', selectedRating);
        });
    });

    
    document.getElementById("searchbtn").onclick = handleSearch;

    function updateNumValue(value) {
        numoutput.innerText = `${value} 家`;
    }

    const moreRegionsBtn = document.getElementById('moreRegionsBtn');
    const moreRegions = document.getElementById('moreRegions');

    moreRegionsBtn.addEventListener('click', () => {
        moreRegions.classList.toggle('hidden');
        moreRegionsBtn.textContent = moreRegions.classList.contains('hidden') ? '查看更多' : '隱藏部分區域';
    });


    async function handleSearch() {

        const searchword = document.getElementById("searchword").value;
//        const searchdistance = slider.value;
//        const selectedAreas = Array.from(document.querySelectorAll('.filter-options input:checked'))
//                                                                .map(checkbox => checkbox.value);
        const MaxItemNum = numslider.value;

        console.log('searchword:', searchword);
//        console.log('searchdistance:', searchdistance);
//        console.log('selectedRating:', selectedRating);
//        console.log('selectedAreas:', selectedAreas);
        console.log('searchMaxNum:', MaxItemNum);

        const resultElement = document.getElementById("result");
        let loadingElement = document.createElement("div");
        loadingElement.className = "loading-animation";
        resultElement.innerHTML = "";
        resultElement.appendChild(loadingElement);

        let currentDots = 1;
        const interval = setInterval(() => {
            loadingElement.innerText = `Loading${'.'.repeat(currentDots)}`;
            currentDots = (currentDots < 3) ? currentDots + 1 : 1;
        }, 500);

        try {
            const response = await fetch("/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ searchword, MaxItemNum })
            });

            clearInterval(interval);
            resultElement.innerHTML = "";

            if (response.ok) {
                const data = await response.text();
                const Data = data.replace(/^"(.*)"$/, '$1');
                document.getElementById("result").innerHTML = "<div class='result-title'><h2>搜尋結果：</h2><div class='button-part'><button id='send-all-button'>生成Hashtag</button><button id='select-all-button'>全選</button></div></div>"+Data;
        
                document.getElementById("select-all-button").addEventListener("click", () => {
                    const checkboxes = document.querySelectorAll('#result .place-check input[type="checkbox"]');
                    checkboxes.forEach(checkbox => {
                        checkbox.checked = true;
                    });
                    console.log('select all');
                });

                const placeItemNames = document.querySelectorAll('.place-item-name');
                if (placeItemNames.length > 0) {
                    createConfirmButton();
                }
                
                const confirmButton = document.getElementById("confirm-btn");
                confirmButton.addEventListener("click", function() {
                    const checkboxes = document.querySelectorAll('.place-check input[type="checkbox"]');
                    checkboxes.forEach(function(checkbox) {
                        const placeItem = checkbox.closest('.place-item');
                        if (!checkbox.checked) {
                            placeItem.style.display = 'none'; 
                        }
                    });
                    createAddToFolderButton();
                });

            } else {
                const errorData = await response.json();
                console.error("Error details:", errorData);
                document.getElementById("result").innerText = "發生錯誤！" + JSON.stringify(errorData);
            }


        } catch (error) {
            console.error("Error during fetch:", error);
            document.getElementById("result").innerText = "發生錯誤！請稍後再試。";
        }

        const regionCheckboxes = document.querySelectorAll("#regionOptions input[type='checkbox']");
        const resultContainer = document.getElementById("result");

        regionCheckboxes.forEach(checkbox => {
            checkbox.addEventListener("change", updateResults);
        });

        function updateResults() {
            const selectedRegions = Array.from(regionCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);

            const allPlaceItems = resultContainer.querySelectorAll(".place-item");

            allPlaceItems.forEach(placeItem => {
                const district = placeItem.querySelector(".place-item-name").getAttribute("data-district");

                if (selectedRegions.length === 0 || selectedRegions.includes(district)) {
                    placeItem.style.display = "";
                } else {
                    placeItem.style.display = "none";
                }
            });
        }

        updateResults();

        const addCheckboxListeners = () => {
            const checkboxes = document.querySelectorAll(".filter-options input[type='checkbox']");
            checkboxes.forEach(checkbox => {
                if (!checkbox.hasAttribute("data-listener")) {
                    checkbox.addEventListener("change", updateResults);
                    checkbox.setAttribute("data-listener", "true");
                }
            });
        };

        addCheckboxListeners();

        moreRegionsBtn.addEventListener('click', () => {
            moreRegionsDiv.classList.toggle('hidden');
            moreRegionsBtn.textContent = moreRegionsDiv.classList.contains('hidden') ? '查看更多' : '隱藏部分區域';
            addCheckboxListeners();
        });


        document.getElementById("send-all-button").addEventListener("click", async () => {
            console.log('processing');
            const checkboxes = document.querySelectorAll('.place-check input[type="checkbox"]:checked');
            const placeItems = Array.from(checkboxes).map(checkbox => checkbox.closest('.place-item'));
            const results = [];
            
            for (const placeItem of placeItems) {
                const ratingElement = placeItem.querySelector('.place-item-rating');
                if (!ratingElement) {
                    console.warn('Missing .place-item-rating for:', placeItem);
                    continue;
                }
            
                let loadingElement = ratingElement.parentNode.querySelector('.place-item-loading, .hashtag-response');
            
                if (!loadingElement) {
                    loadingElement = document.createElement('div');
                    loadingElement.className = 'place-item-loading';
                    ratingElement.parentNode.appendChild(loadingElement);
                } else {
                    loadingElement.innerText = '';
                    loadingElement.className = 'place-item-loading';
                }
            
                let currentDots = 2;
            
                const interval = setInterval(() => {
                    loadingElement.innerText = '.'.repeat(currentDots); 
                    currentDots = (currentDots < 6) ? currentDots + 1 : 2;
                }, 500); 
            
                try {
                    const name = placeItem.querySelector('.place-item-name').getAttribute("data-name");
                    const user_ratings_total = placeItem.querySelector('.place-item-name').getAttribute("data-user_ratings_total");
            
                    const response = await fetch("/hashtag", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ searchword: name, reviewsnum: user_ratings_total }),
                    });
            
                    clearInterval(interval);
            
                    if (response.ok) {
                        const data = await response.text();
                        const Data = data.replace(/^"(.*)"$/, '$1');
                        loadingElement.innerHTML = Data;
                        loadingElement.classList.remove('place-item-loading');
                        loadingElement.classList.add('hashtag-response');
                        results.push({ name, hashtag: Data });
                    } else {
                        loadingElement.innerText = 'Unable to obtain';
                        loadingElement.classList.remove('place-item-loading');
                        loadingElement.classList.add('hashtag-response');
                    }
                } catch (error) {
                    clearInterval(interval);
                    console.error(`Error generating hashtag for ${name}:`, error);
                    loadingElement.innerText = 'Error!';
                    loadingElement.classList.remove('place-item-loading');
                    loadingElement.classList.add('hashtag-response');
                }
            }
            
            console.log("All hashtags processed:", results);
        });
            
    function createConfirmButton() {
        const resultContainer = document.getElementById("result");

        let confirmButton = resultContainer.querySelector("#confirm-btn");
        if (!confirmButton) {
            confirmButton = document.createElement("button");
            confirmButton.id = "confirm-btn";
            confirmButton.innerText = "確認";
            confirmButton.classList.add("confirm-btn-style");
            resultContainer.appendChild(confirmButton);

            confirmButton.addEventListener("click", handleConfirmClick);
        }
    }

    function handleConfirmClick() {
        console.log("已確認，保留勾選項目");

        const checkboxes = document.querySelectorAll('.place-check input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            const placeItem = checkbox.closest('.place-item');
            if (!checkbox.checked) {
                placeItem.style.display = 'none';
            }
        });

        createAddToFolderButton();
    }

    function createAddToFolderButton() {
        const resultContainer = document.getElementById("result");
        console.log('createAddtoFolderBtn');
        if (!inputField) {
            inputField = document.createElement("input");
            inputField.type = "text";
            inputField.placeholder = "輸入資料夾名稱";
            inputField.classList.add("input-folder-name");
            resultContainer.appendChild(inputField);
        }

        if (!addToFolderButton) {
            addToFolderButton = document.createElement("button");
            addToFolderButton.id = "add-folder-btn";
            addToFolderButton.innerText = "確認，加入資料夾";
            addToFolderButton.classList.add("add-folder-btn-style");
            resultContainer.appendChild(addToFolderButton);

            addToFolderButton.addEventListener("click", handleAddToFolder);
        }
    }

    async function fetchStoreNames() {
        const { data, error } = await supabase
            .from('foldername')
            .select('store_name')
    
        if (error) {
            console.error('Error fetching store names:', error);
            return [];
        }
    
        const existingStoreNames = data.map(item => item.store_name);
        console.log('Store Names:', storeNames);
    
        return existingStoreNames;
    }
    

    async function handleAddToFolder() {
        const folderName = inputField.value.trim();
        if (!folderName) {
            console.log("請輸入資料夾名稱");
            return;
        }

        const checkboxes = document.querySelectorAll('.place-check input[type="checkbox"]:checked');
        if (checkboxes.length === 0) {
            console.log("請選擇至少一個店家");
            return;
        }
        
        const existingStoreNames = [];
    
        const fetchedNames = await fetchStoreNames();
        existingStoreNames.push(...fetchedNames);
    
        const selectedPlaces = Array.from(checkboxes).map(checkbox => {
            const placeItem = checkbox.closest('.place-item');
            const placeNameElement = placeItem.querySelector('.place-item-name');
    
            const storeName = placeNameElement.getAttribute('data-name') || null;

            const hashtagElement = placeItem.querySelector('.hashtag-response');
            const Hashtag = hashtagElement ? hashtagElement.innerText : null;

            if (existingStoreNames.includes(storeName)) {
                return null;
            }
    
            return {
                store_name: storeName,
                coordinates: `(${parseFloat(placeNameElement.getAttribute('data-lat')) || null}, ${parseFloat(placeNameElement.getAttribute('data-lng')) || null})`,
                photo_url: placeNameElement.getAttribute('data-photo_url') || null,
                rating: parseFloat(placeNameElement.getAttribute('data-rating')) || null,
                user_ratings_total: parseInt(placeNameElement.getAttribute('data-user_ratings_total'), 10) || null,
                business_status: placeNameElement.getAttribute('data-status') || null,
                district: placeNameElement.getAttribute('data-district') || null,
                hashtag: Hashtag || null 
            };
        }).filter(place => place !== null);
    
        console.log('Selected Places:', selectedPlaces);
    
        try {
            const { data, error } = await supabase
                .from(folderName) 
                .insert(selectedPlaces);
    
            if (error) {
                console.error('Error inserting data:', error);
                return;
            }
    
            console.log('Data inserted:', data);
        } catch (error) {
            console.error('Unexpected error:', error);
        }
    }

    
    function highlightStars(index) {
        stars.forEach((star, i) => {
            if (i <= index) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }
};

const container = document.getElementById('result');

container.addEventListener('click', async function(event) {
    if (event.target.classList.contains('place-item-name')) {
        const selectedItem = event.target.textContent;
        const userRatingsTotal = event.target.getAttribute('data-user_ratings_total');
        console.log(selectedItem);

        const ratingElement = event.target.closest('.place-item').querySelector('.place-item-rating');
        let loadingElement = ratingElement.parentNode.querySelector('.place-item-loading, .hashtag-response');

        if (!loadingElement) {
            loadingElement = document.createElement('div');
            loadingElement.className = 'place-item-loading';
            ratingElement.parentNode.insertBefore(loadingElement, ratingElement.nextSibling);
        } else {
            loadingElement.innerText = '';
            loadingElement.className = 'place-item-loading';
        }

        let currentDots = 2;

        // dynamic loading
        const interval = setInterval(() => {
            loadingElement.innerText = '.'.repeat(currentDots); 
            currentDots = (currentDots < 6) ? currentDots + 1 : 2;
        }, 500); 

        try {
            const response = await fetch("/hashtag", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ searchword: selectedItem, reviewsnum: userRatingsTotal })
            });

            clearInterval(interval);
            
            if (response.ok) {
                const data = await response.text();
                const Data = data.replace(/^"(.*)"$/, '$1');
                loadingElement.innerHTML = Data; 
                loadingElement.classList.remove('place-item-loading');
                loadingElement.classList.add('hashtag-response');
            } else {
                loadingElement.innerText = 'Unable to obtain';
                loadingElement.classList.remove('place-item-loading');
                loadingElement.classList.add('hashtag-response');
            }
        } catch (error) {
            console.error("Error during fetch:", error);
            clearInterval(interval);
            loadingElement.innerText = '發生錯誤！';
            loadingElement.classList.remove('place-item-loading');
            loadingElement.classList.add('hashtag-response');
        }
    }
})
})