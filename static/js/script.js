document.addEventListener("DOMContentLoaded", function () {

    const reportPage = document.querySelector("[data-threatlens-report]");

    // Only run on the report page
    if (!reportPage) {
        return;
    }

    const aiStatus = document.getElementById("ai-status");

    if (aiStatus) {
        aiStatus.textContent = "⏳ Generating AI security insights...";
    }

    fetch("/api/ai-advice")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {

            if (!data.success || !data.ai) {
                showAIError();
                return;
            }

            renderAIAdvice(data.ai);

            if (aiStatus) {
                aiStatus.textContent = "✓ AI analysis ready";
            }
        })
        .catch(function (error) {

            console.error("ThreatLens AI error:", error);

            showAIError();
        });


    function renderAIAdvice(ai) {

        // Overall summary
        if (ai.overall_summary) {

            const summary =
                document.getElementById("ai-overall-summary");

            if (summary) {
                summary.textContent = ai.overall_summary;
            }
        }


        // Priority findings
        if (ai.priority_findings) {

            ai.priority_findings.forEach(function (finding) {

                const block = document.querySelector(
                    '[data-ai-finding="' +
                    finding.category +
                    '"]'
                );

                if (!block) {
                    return;
                }

                const why = block.querySelector(".ai-why");

                if (why) {
                    why.textContent =
                        finding.why_it_matters || "";
                }


                const actions =
                    block.querySelector(".ai-actions");

                if (actions) {

                    actions.innerHTML = "";

                    (finding.recommended_actions || [])
                        .forEach(function (action) {

                            const li =
                                document.createElement("li");

                            li.textContent = action;

                            actions.appendChild(li);
                        });
                }
            });
        }


        // Roadmap
        if (ai.roadmap) {

            Object.keys(ai.roadmap).forEach(function (bucket) {

                const phase = ai.roadmap[bucket];

                const block = document.querySelector(
                    '[data-ai-roadmap="' +
                    bucket +
                    '"]'
                );

                if (!block || !phase) {
                    return;
                }


                const summary =
                    block.querySelector(".ai-phase-summary");

                if (summary) {
                    summary.textContent =
                        phase.summary || "";
                }


                const actions =
                    block.querySelector(".ai-phase-actions");

                if (actions) {

                    actions.innerHTML = "";

                    (phase.action_items || [])
                        .forEach(function (action) {

                            const li =
                                document.createElement("li");

                            li.textContent = action;

                            actions.appendChild(li);
                        });
                }
            });
        }
    }


    function showAIError() {

        if (aiStatus) {

            aiStatus.textContent =
                "⚠ AI advice is temporarily unavailable. " +
                "Your rule-based assessment is still valid.";
        }
    }

});
