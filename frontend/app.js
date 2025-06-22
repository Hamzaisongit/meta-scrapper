document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const downloadBtn = document.getElementById("download-btn");
    const keywordInput = document.getElementById("keyword");
    const statusMessage = document.getElementById("status-message");
    const postCount = document.getElementById("post-count");
    const postsContainer = document.getElementById("posts-container");

    let isFetching = false;
    let fetchedPosts = [];
    let afterCursor = null;

    startBtn.addEventListener("click", () => {
        isFetching = true;
        startBtn.disabled = true;
        stopBtn.disabled = false;
        keywordInput.disabled = true;
        statusMessage.textContent = "Fetching...";
        fetchedPosts = [];
        afterCursor = null;
        postsContainer.innerHTML = "";
        fetchPosts();
    });

    stopBtn.addEventListener("click", () => {
        isFetching = false;
        startBtn.disabled = false;
        stopBtn.disabled = true;
        keywordInput.disabled = false;
        statusMessage.textContent = "Stopped";
    });

    downloadBtn.addEventListener("click", () => {
        if (fetchedPosts.length === 0) {
            alert("No data to download.");
            return;
        }
        downloadCSV(fetchedPosts);
    });

    async function fetchPosts() {
        if (!isFetching) return;

        const keyword = keywordInput.value.trim();
        
        try {
            const response = await fetch("http://127.0.0.1:5000/scrape", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ keyword, after_cursor: afterCursor }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || "Failed to fetch data");
            }

            const data = await response.json();

            if (data.status === "success") {
                fetchedPosts.push(...data.posts);
                postCount.textContent = fetchedPosts.length;
                displayPosts(data.posts);
                
                if (data.page_info.has_next_page && isFetching) {
                    afterCursor = data.page_info.end_cursor;
                    setTimeout(fetchPosts, 1000); // Add a small delay
                } else {
                    isFetching = false;
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                    keywordInput.disabled = false;
                    statusMessage.textContent = "Finished";
                }
            } else {
                throw new Error(data.message || "An unknown error occurred");
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
            statusMessage.textContent = `Error: ${error.message}`;
            isFetching = false;
            startBtn.disabled = false;
            stopBtn.disabled = true;
            keywordInput.disabled = false;
        }
    }

    function displayPosts(posts) {
        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.className = "post";
            postElement.innerHTML = `
                <div class="post-header">
                    <span>@${post.username}</span>
                </div>
                <div class="post-query">
                    <strong>Query:</strong> ${post.user_query}
                </div>
            `;
            postsContainer.appendChild(postElement);
        });
    }

    function downloadCSV(posts) {
        const headers = ["username", "user_query", "ai_response"];
        const csvContent = [
            headers.join(","),
            ...posts.map(post => [
                `"${post.username}"`,
                `"${post.user_query.replace(/"/g, '""')}"`,
                `"${post.ai_response.replace(/"/g, '""')}"`
            ].join(","))
        ].join("\n");

        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "meta_posts.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}); 