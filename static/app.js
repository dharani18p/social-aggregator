// // script.js

// document.addEventListener("DOMContentLoaded", () => {
//     // GitHub Elements
//     const githubOwnerInput = document.getElementById("github-owner");
//     const githubRepoInput = document.getElementById("github-repo");
//     const githubReposInput = document.getElementById("github-repos");
//     const githubResults = document.getElementById("github-results");

//     // Reddit Elements
//     const redditSubredditInput = document.getElementById("reddit-subreddit");
//     const redditResults = document.getElementById("reddit-results");

//     // Helper function to display errors
//     function displayError(container, message) {
//         container.innerHTML = `<p class="error">❌ ${message}</p>`;
//     }

//     // Helper function to display loading
//     function displayLoading(container, message) {
//         container.innerHTML = `<p class="loading">⏳ ${message}</p>`;
//     }

//     // ---------------- GitHub Buttons ----------------
//     document.getElementById("get-top-issues").addEventListener("click", async () => {
//         const owner = githubOwnerInput.value.trim();
//         const repo = githubRepoInput.value.trim();

//         if (!owner || !repo) {
//             displayError(githubResults, "Please enter both owner and repo name.");
//             return;
//         }

//         displayLoading(githubResults, "Loading top issues...");

//         try {
//             const response = await fetch(`/api/github/top-issues?owner=${encodeURIComponent(owner)}&repo=${encodeURIComponent(repo)}`);

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP ${response.status}`);
//             }

//             const data = await response.json();

//             if (data.length === 0) {
//                 githubResults.innerHTML = "<p>No open issues found.</p>";
//             } else {
//                 githubResults.innerHTML = "<h3>Top 5 Issues by Comments:</h3>" + data
//                     .map(
//                         (issue, index) =>
//                             `<p>${index + 1}. <a href="${issue.url}" target="_blank">${issue.title}</a> <strong>(💬 ${issue.comments} comments)</strong></p>`
//                     )
//                     .join("");
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             displayError(githubResults, `Failed to fetch data: ${error.message}`);
//         }
//     });

//     document.getElementById("find-top-author-gh").addEventListener("click", async () => {
//         const owner = githubOwnerInput.value.trim();
//         const repo = githubRepoInput.value.trim();

//         if (!owner || !repo) {
//             displayError(githubResults, "Please enter both owner and repo name.");
//             return;
//         }

//         displayLoading(githubResults, "Finding top author...");

//         try {
//             const response = await fetch(`/api/github/top-author?owner=${encodeURIComponent(owner)}&repo=${encodeURIComponent(repo)}`);

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP ${response.status}`);
//             }

//             const data = await response.json();

//             if (data.author === "N/A" || data.issue_count === 0) {
//                 githubResults.innerHTML = `<p>No issues found in this repository.</p>`;
//             } else {
//                 githubResults.innerHTML = `<p class="success">👤 Top Author: <strong>${data.author}</strong> with <strong>${data.issue_count}</strong> open issues.</p>`;
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             displayError(githubResults, `Failed to fetch data: ${error.message}`);
//         }
//     });

//     document.getElementById("find-top-repo").addEventListener("click", async () => {
//         const owner = githubOwnerInput.value.trim();
//         const repos = githubReposInput.value.trim();

//         if (!owner || !repos) {
//             displayError(githubResults, "Please enter owner and comma-separated repos.");
//             return;
//         }

//         displayLoading(githubResults, "Finding top repo...");

//         try {
//             const response = await fetch(`/api/github/top-repo?owner=${encodeURIComponent(owner)}&repos=${encodeURIComponent(repos)}`);

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP ${response.status}`);
//             }

//             const data = await response.json();
//             githubResults.innerHTML = `<p class="success">📦 Top Repo: <strong>${data.repo}</strong> with <strong>${data.open_issues}</strong> open issues.</p>`;
//         } catch (error) {
//             console.error("Error:", error);
//             displayError(githubResults, `Failed to fetch data: ${error.message}`);
//         }
//     });

//     // ---------------- Reddit Buttons ----------------
//     document.getElementById("get-top-posts").addEventListener("click", async () => {
//         const subreddit = redditSubredditInput.value.trim();

//         if (!subreddit) {
//             displayError(redditResults, "Please enter a subreddit name.");
//             return;
//         }

//         displayLoading(redditResults, "Loading top posts...");

//         try {
//             const response = await fetch(`/api/reddit/top-posts?subreddit=${encodeURIComponent(subreddit)}`);

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP ${response.status}`);
//             }

//             const data = await response.json();

//             if (data.length === 0) {
//                 redditResults.innerHTML = "<p>No posts found.</p>";
//             } else {
//                 redditResults.innerHTML = "<h3>Top 5 Posts by Upvotes:</h3>" + data
//                     .map(
//                         (post, index) =>
//                             `<p>${index + 1}. ${post.title} by <strong>${post.author}</strong> <strong>(⬆ ${post.upvotes} upvotes)</strong></p>`
//                     )
//                     .join("");
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             displayError(redditResults, `Failed to fetch data: ${error.message}`);
//         }
//     });

//     document.getElementById("find-top-author-rd").addEventListener("click", async () => {
//         const subreddit = redditSubredditInput.value.trim();

//         if (!subreddit) {
//             displayError(redditResults, "Please enter a subreddit name.");
//             return;
//         }

//         displayLoading(redditResults, "Finding top author...");

//         try {
//             const response = await fetch(`/api/reddit/top-author?subreddit=${encodeURIComponent(subreddit)}`);

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP ${response.status}`);
//             }

//             const data = await response.json();

//             if (data.author === "N/A" || data.posts === 0) {
//                 redditResults.innerHTML = `<p>No posts found in this subreddit.</p>`;
//             } else {
//                 redditResults.innerHTML = `<p class="success">👤 Top Author: <strong>${data.author}</strong> with <strong>${data.posts}</strong> posts today.</p>`;
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             displayError(redditResults, `Failed to fetch data: ${error.message}`);
//         }
//     });
// });