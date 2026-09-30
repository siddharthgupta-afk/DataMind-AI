// ============================================================
// DATAMIND AI — FRONTEND
// Personalized Product Recommendation Dashboard
// ============================================================

const API_BASE_URL = "";
const INSIGHTS_ENDPOINT = "/customer";

// DOM ELEMENTS
const customerInput = document.getElementById("customerId");
const recommendBtn = document.getElementById("recommendBtn");

const customerSection = document.getElementById("customerSection");
const emptyState = document.getElementById("emptyState");
const errorMessage = document.getElementById("errorMessage");

const customerNumber = document.getElementById("customerNumber");
const clusterNumber = document.getElementById("clusterNumber");

const metricOrders =
    document.getElementById("metricOrders");

const metricSpent =
    document.getElementById("metricSpent");

const metricRecency =
    document.getElementById("metricRecency");

const metricSegment =
    document.getElementById("metricSegment");

const rScore =
    document.getElementById("rScore");

const fScore =
    document.getElementById("fScore");

const mScore =
    document.getElementById("mScore");

const rfmTotal =
    document.getElementById("rfmTotal");

const rfmOverall =
    document.getElementById("rfmOverall");

const rfmLabel =
    document.getElementById("rfmLabel");

const customerInsightTitle =
    document.getElementById("customerInsightTitle");

const customerInsightText =
    document.getElementById("customerInsightText");

const insightRfm =
    document.getElementById("insightRfm");

const recommendationCount =
    document.getElementById("recommendationCount");

const recommendationsContainer =
    document.getElementById("recommendations");


// ============================================================
// PRODUCT ICONS
// ============================================================

const categoryIcons = {
    "Clothing": "◈",
    "Beauty": "✦",
    "Electronics": "⌁",
    "Home & Kitchen": "⌂",
    "Sports": "◎",
    "Books": "▤",
    "Accessories": "◇",
    "Footwear": "◉"
};


// ============================================================
// FORMAT PRICE
// ============================================================

function formatPrice(price) {

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2
    }).format(price);

}


// ============================================================
// GET CATEGORY ICON
// ============================================================

function getCategoryIcon(category) {

    return categoryIcons[category] || "✦";

}


// ============================================================
// LOADING STATE
// ============================================================

function setLoading(isLoading) {

    if (isLoading) {

        recommendBtn.disabled = true;

        recommendBtn.innerHTML = `
            Analyzing
            <span class="loading-dots">•••</span>
        `;

    } else {

        recommendBtn.disabled = false;

        recommendBtn.innerHTML = `
            Get Recommendations
            <span>→</span>
        `;

    }

}


// ============================================================
// SHOW ERROR
// ============================================================

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

    customerSection.classList.add("hidden");

}


// ============================================================
// CLEAR ERROR
// ============================================================

function clearError() {

    errorMessage.classList.add("hidden");

    errorMessage.textContent = "";

}


// ============================================================
// CREATE PRODUCT CARD
// ============================================================

function createProductCard(product, index) {

    const score = Number(product.recommendation_score);

    const percentage = Math.min(
        Math.max(score * 100, 0),
        100
    );

    const icon = getCategoryIcon(product.category);

    const card = document.createElement("article");

    card.className = "product-card";

    // Small staggered animation
    card.style.animationDelay = `${index * 80}ms`;

    card.innerHTML = `

        <div class="product-rank">
            #${product.rank}
        </div>

        <div class="product-icon">
            ${icon}
        </div>

        <p class="product-category">
            ${product.category}
        </p>

        <h4 class="product-name">
            ${product.product_name}
        </h4>

        <p class="product-price">
            ${formatPrice(product.price)}
        </p>

        <div class="score-section">

            <div class="score-row">

                <span>
                     RECOMMENDATION SCORE
                </span>

                <span class="score-value">
                    ${percentage.toFixed(1)}%
                </span>

            </div>

            <div class="score-bar">

                <div
                    class="score-fill"
                    style="width: ${percentage}%"
                ></div>

            </div>

        </div>
    `;

    return card;

}


// ============================================================
// RENDER RECOMMENDATIONS
// ============================================================

function renderRecommendations(data) {

    recommendationsContainer.innerHTML = "";

    const recommendations = data.recommendations || [];

    // CUSTOMER INFORMATION

    customerNumber.textContent =
        `#${data.customer_id}`;

    clusterNumber.textContent =
        data.cluster;

    const insights = data.insights;

    
    metricOrders.textContent =
        insights.total_orders;

    metricSpent.textContent =
        formatPrice(insights.total_spent);

    metricRecency.textContent =
        `${insights.recency_days} days`;

    metricSegment.textContent =
        insights.customer_segment;
    
    rScore.textContent =
        insights.r_score;

    fScore.textContent =
        insights.f_score;

    mScore.textContent =
        insights.m_score;

    rfmTotal.textContent =
        insights.rfm_score;

    rfmOverall.textContent =
        insights.rfm_score;

    rfmLabel.textContent =
        insights.customer_segment;

// ============================================================
// DATAMIND INSIGHT
// ============================================================

customerInsightTitle.textContent =
    `Customer #${insights.customer_id} intelligence profile`;

customerInsightText.textContent =
    `This customer has ${insights.total_orders} completed orders ` +
    `with ${formatPrice(insights.total_spent)} in total spend. ` +
    `Their RFM score is ${insights.rfm_score}/15 and they are ` +
    `classified as ${insights.customer_segment}. ` +
    `Recommendations combine behavioral and purchase signals.`;

insightRfm.textContent =
    insights.rfm_score;

    recommendationCount.textContent =
        `${recommendations.length} products`;


    // CREATE PRODUCT CARDS

    recommendations.forEach((product, index) => {

        const card =
            createProductCard(product, index);

        recommendationsContainer.appendChild(card);

    });


    // SWITCH UI

    emptyState.classList.add("hidden");

    customerSection.classList.remove("hidden");

}

// ============================================================
// FETCH CUSTOMER INSIGHTS
// ============================================================

async function getCustomerInsights(customerId) {

    const response = await fetch(
        `${API_BASE_URL}${INSIGHTS_ENDPOINT}/${customerId}/insights`
    );

    if (!response.ok) {

        if (response.status === 404) {

            throw new Error(
                `No customer insights found for ${customerId}.`
            );
        }

        throw new Error(
            "Unable to retrieve customer insights."
        );
    }

    return await response.json();
}

// ============================================================
// FETCH RECOMMENDATIONS
// ============================================================

async function getRecommendations() {

    const customerId =
        customerInput.value.trim();


    // VALIDATION

    if (!customerId) {

        showError(
            "Please enter a customer ID."
        );

        return;
    }


    if (Number(customerId) <= 0) {

        showError(
            "Customer ID must be greater than 0."
        );

        return;
    }


    clearError();

    setLoading(true);


    try {

        const response = await fetch(
            `${API_BASE_URL}/recommendations/${customerId}`
        );


        // CUSTOMER NOT FOUND / API ERROR

        if (!response.ok) {

            if (response.status === 404) {

                throw new Error(
                    `Customer ${customerId} was not found.`
                );

            }

            throw new Error(
                "Unable to retrieve recommendations."
            );

        }


        const data = await response.json();

        const insights =
            await getCustomerInsights(customerId);

        data.insights = insights;


        if (
            !data.recommendations ||
            data.recommendations.length === 0
        ) {

            throw new Error(
                `No recommendations found for customer ${customerId}.`
            );

        }


        renderRecommendations(data);

    }

    catch (error) {

        console.error(
            "DataMind API Error:",
            error
        );


        // Fetch throws TypeError when API cannot be reached

        if (error instanceof TypeError) {

            showError(
                "DataMind AI API is offline. Make sure the FastAPI server is running."
            );

        } else {

            showError(error.message);

        }

    }

    finally {

        setLoading(false);

    }

}


// ============================================================
// BUTTON EVENT
// ============================================================

recommendBtn.addEventListener(
    "click",
    getRecommendations
);


// ============================================================
// ENTER KEY SUPPORT
// ============================================================

customerInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            getRecommendations();

        }

    }
);


// ============================================================
// INPUT CLEANUP
// ============================================================

customerInput.addEventListener(
    "input",
    function () {

        clearError();

    }
);


// ============================================================
// STARTUP
// ============================================================

console.log(
    "%cDataMind AI",
    "font-size:20px;font-weight:bold;color:#7c5cff;"
);

console.log(
    "Recommendation frontend initialized."
);