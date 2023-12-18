var fetchData;
var validateFormCount = 0;
function validateFormAndSendData(event) {
  let isValid = true;
  let errorMsg = "";

  const searchKeyword = document.getElementById("searchKeyword").value;
  const minPrice = document.getElementById("minPrice").value;
  const maxPrice = document.getElementById("maxPrice").value;

  //   if (!searchKeyword) {
  //     errorMsg = "Keyword is required!";
  //     document.getElementById("keywordErrorMsg").innerText = errorMsg;
  //     isValid = false;
  //   } else {
  //     document.getElementById("keywordErrorMsg").innerText = ""; // Clearing any previous error messages
  //   }

  if (minPrice < 0 || maxPrice < 0) {
    errorMsg =
      "Price Range values cannot be negative! Please try a value greater than or equal to 0.0";
    // document.getElementById("priceErrorMsg").innerText = errorMsg;
    alert(errorMsg);
    isValid = false;
  } else if (parseFloat(minPrice) > parseFloat(maxPrice)) {
    errorMsg =
      "Oops! Lower price limit cannot be greater than upper price limit! Please try again.";
    // document.getElementById("priceErrorMsg").innerText = errorMsg;
    alert(errorMsg);
    isValid = false;
  }

  event.preventDefault();

  const formData = new FormData(document.getElementById("searchForm"));
  const queryString = new URLSearchParams(formData).toString();

  if (isValid) {
    fetch("/search?" + queryString)
      // .then((response) => console.log(response))
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        console.log(data.keyword);
        // if (data.total_results == 0) {
        //   document.getElementById("cardResult").style.display = "none";
        // }
        // resultCount = data.total_results;
        // setTimeout(
        //   function () {
        //     if (data.total_results == 0) {
        //       document.getElementById("cardResult").style.display = "none";
        //       document.getElementById("showmore").style.display = "none";
        //       document.getElementById("showless").style.display = "none";
        //       document.getElementById("itemDetails").style.display = "none";
        //       document.getElementById("noResults").style.display = "block";
        //     } else {
        //       document.getElementById("cardResult").style.display = "block";
        //       document.getElementById("showmore").style.display = "block";
        //       document.getElementById("showless").style.display = "none";
        //       document.getElementById("itemDetails").style.display = "none";
        //       document.getElementById("noResults").style.display = "none";
        //     }
        //   },
        //   (validateFormCount) => {
        //     if (validateFormCount == 0) return 1500;
        //     else {
        //       validateFormCount = validateFormCount + 1;
        //       return 800;
        //     }
        //   }
        // );
        if (data.total_results == 0) {
          document.getElementById("cardResult").style.display = "none";
          document.getElementById("showmore").style.display = "none";
          document.getElementById("showless").style.display = "none";
          document.getElementById("itemDetails").style.display = "none";
          document.getElementById("noResults").style.display = "block";
        } else {
          document.getElementById("cardResult").style.display = "block";
          document.getElementById("showmore").style.display = "block";
          document.getElementById("showless").style.display = "none";
          document.getElementById("itemDetails").style.display = "none";
          document.getElementById("noResults").style.display = "none";
        }
        document.getElementById("displayKeyword").textContent = data.keyword;
        document.getElementById("totalResults").textContent =
          data.total_results;
        // 渲染数据
        fetchData = data;
        // console.log("rendering results");
        // renderResults(data.responseItems);
      })
      .then((data) => {
        console.log("rendering results");
        renderResults(fetchData.responseItems);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  // setTimeout(function () {
  //   // 这里是等待1秒后执行的代码
  //   console.log("等待了1秒后执行");
  // }, 5000); // 1000毫秒等于1秒

  // console.log(data);

  return isValid;
}

let resultCount = 0;

let currentDisplayCount = 3; // 默认显示3个结果

function renderResults(items) {
  const resultsContainer = document.getElementById("result");
  // 清空现有的结果
  resultsContainer.innerHTML = "";

  // 仅展示当前数量的结果
  for (let i = 0; i < currentDisplayCount && i < items.length; i++) {
    resultsContainer.appendChild(createResultCard(items[i]));
  }
}

// function createResultCard(item) {
//   const card = document.createElement("div");
//   card.className = "card";

//   // 为了简单起见，这里只为每个卡片添加了标题。您可以按需扩展此部分。
//   const title = document.createElement("h3");
//   title.textContent = item.title;
//   card.appendChild(title);

//   return card;
// }
var tempText = "";
var ebayDefaultUrl = "https://thumbs1.ebaystatic.com/pict/04040_0.jpg";
var expectedDefaultUrl = "https://csci571.com/hw/hw6/images/ebay_default.jpg";

function getSingleItem(itemId) {
  // Assuming your Flask backend expects a GET request with itemId as a parameter
  fetch(`/showItem?itemId=${itemId}`)
    .then((response) => response.json())
    .then((data) => {
      // Handle the returned data from Flask here.
      // For now, let's just log it to the console.
      console.log(data);
      document.getElementById("cardResult").style.display = "none";
      populateTable(data);
    })
    .catch((error) => {
      console.error("Error fetching item details:", error);
    });
}

function populateTable(data) {
  document.getElementById("itemDetails").style.display = "block";
  const tableBody = document.querySelector("#data-table tbody");

  // Clear the existing rows if any
  tableBody.innerHTML = "";

  data.forEach((item) => {
    const row = tableBody.insertRow();
    const cell1 = row.insertCell(0);
    cell1.style.width = "150px";
    const cell2 = row.insertCell(1);

    // 创建一个 <strong> 元素来包装 item.key 的文本内容
    const strong = document.createElement("strong");
    strong.textContent = item.key;
    cell1.appendChild(strong);

    if (item.key === "Photo") {
      const img = document.createElement("img");
      img.src = item.value;
      img.id = "img_id_profile";
      img.alt = "Photo";
      img.width = 200;
      cell2.appendChild(img);
    } else if (item.key === "eBay Link") {
      const a = document.createElement("a");
      a.href = item.value;
      a.target = "_blank"; // 使链接在新窗口/选项卡中打开
      a.innerText = "eBay Product Link";
      cell2.appendChild(a);
    } else {
      cell2.textContent = item.value;
    }
  });
}

function createResultCard(item) {
  const box = document.createElement("div");
  box.className = "box content-box";
  box.id = item.itemId; // Setting the ID based on itemId from the item
  box.onclick = () => getSingleItem(item.itemId); // Assigning onclick function with itemId as a parameter
  // box.addEventListener("click", expand); // assuming you have an 'expand' function

  const img = document.createElement("img");
  img.id = "img_id";
  img.src =
    item["galleryURL"] == null || item["galleryURL"] == ""
      ? expectedDefaultUrl
      : item["galleryURL"];
  box.appendChild(img);

  const rightContent = document.createElement("div");
  rightContent.className = "right-content";

  const productLink = document.createElement("div");
  productLink.id = "product_link";
  const anchor = document.createElement("a");
  anchor.className = "title_id";
  // anchor.href = item["viewItemURL"];
  // anchor.target = "_blank";
  // var title = item["title"];
  // if (title.length > 45) {
  //   anchor.textContent = title.slice(0, 45) + "...";
  // } else {
  //   anchor.textContent = title;
  // }
  anchor.textContent = item["title"];
  productLink.appendChild(anchor);
  rightContent.appendChild(productLink);

  const categoryDiv = document.createElement("div");
  categoryDiv.id = "cat_id";
  categoryDiv.innerHTML = `<span id='nametag'>Category:</span>${item["categoryName"]}`;
  const categoryLink = document.createElement("a");
  categoryLink.href = item["viewItemURL"];
  categoryLink.target = "_blank";
  categoryLink.addEventListener("click", function (event) {
    event.stopPropagation();
  });
  const categoryImg = document.createElement("img");
  categoryImg.id = "redirect";
  categoryImg.src = "https://csci571.com/hw/hw6/images/redirect.png";
  categoryLink.appendChild(categoryImg);
  categoryDiv.appendChild(categoryLink);
  rightContent.appendChild(categoryDiv);

  // Add Condition
  const conditionDiv = document.createElement("div");
  conditionDiv.id = "cond_id";
  conditionDiv.innerHTML = `Condition: ${item["condition"]}`;
  if (item["topRatedListing"] == "true") {
    const topRatedImg = document.createElement("img");
    topRatedImg.id = "topimg_id";
    topRatedImg.src = "https://csci571.com/hw/hw6/images/topRatedImage.png";
    conditionDiv.appendChild(topRatedImg);
  }
  rightContent.appendChild(conditionDiv);

  // Add Price
  const priceDiv = document.createElement("div");
  priceDiv.id = "price_id";
  let priceHTML = `Price: $${item["currentPrice"]}`;
  if (item["shippingServiceCost"] > 0.0) {
    priceHTML += ` (+ $${item["shippingServiceCost"]} for shipping)`;
  }
  priceDiv.innerHTML = priceHTML;
  rightContent.appendChild(priceDiv);

  box.appendChild(rightContent);

  return box;
}

function showMoreFunc() {
  currentDisplayCount = 10;
  renderResults(fetchData.responseItems); // 'data' 应该是您从后端获得的JSON数据
  currentDisplayCount = 3;
  document.getElementById("showmore").style.display = "none";
  document.getElementById("showless").style.display = "block";
}

function showLessFunc() {
  currentDisplayCount = 3;
  renderResults(fetchData.responseItems);
  document.getElementById("showmore").style.display = "block";
  document.getElementById("showless").style.display = "none";
}

function clearForm() {
  console.log("Clearing form...");
  // Clearing text inputs
  document.getElementById("searchKeyword").value = "";

  // Clearing number inputs
  document.getElementById("minPrice").value = "";
  document.getElementById("maxPrice").value = "";

  // Clearing checkboxes
  var checkboxes = [
    "conditionNew",
    "conditionUsed",
    "conditionVeryGood",
    "conditionGood",
    "conditionAcceptable",
    "returnsAccepted",
    "freeShipping",
    "expeditedShipping",
  ];
  checkboxes.forEach(function (checkboxId) {
    document.getElementById(checkboxId).checked = false;
  });

  // Clearing dropdown select
  document.getElementById("sortingOption").value = "BestMatch";

  // If you have any custom error messages or styles applied, reset them
  var errorMessages = document.querySelectorAll(".error-message");
  errorMessages.forEach(function (msg) {
    msg.textContent = "";
  });
  document.getElementById("cardResult").style.display = "none";
  document.getElementById("itemDetails").style.display = "none";
}

function goBack() {
  document.getElementById("cardResult").style.display = "block";
  document.getElementById("itemDetails").style.display = "none";
}
