function KanyeClient() {
  API_ROOT = "/api/v1";

  let form = document.getElementById("get_quotes_form");
  form.addEventListener("submit", getAndAnalyzeQuotes);

  async function getAndAnalyzeQuotes(event) {
    event.preventDefault();
    document.getElementById("results").style.display = "none";
    document.getElementById("quotes").innerHTML =
      "Wating for some Kanye quotes...";
    let quote_number = document.getElementById("quote_number").value;
    const url = API_ROOT + "/quotes?number=" + quote_number;
    let quotes = await fetch(url)
        .then(handleResponse)
        .then(renderQuotes)
        .catch(function (error) {
          console.log(error);
          document.getElementById("results_status").innerHTML =
            "Can't get quotes now. Sorry :(";
        });
    getQuoteAnalysis(quotes);
  }
  async function handleResponse(response) {
    if (response.ok) {
      return response.json();
    }
    throw new Error();
  }

  async function renderQuotes(quotes_json) {
    let quote_list = document.getElementById("quotes");
    quote_list.innerHTML = "";
    for (quote of quotes_json["quotes"]) {
      let quote_li = document.createElement("li");
      let quote_q = document.createElement("q");
      quote_q.innerHTML = quote;
      quote_li.appendChild(quote_q);
      quote_list.appendChild(quote_li);
    }
    return quotes_json["quotes"];
  }

  async function getQuoteAnalysis(quotes) {
    document.getElementById("results_status").innerHTML =
      "Wating for sentiment analysis...";
    fetch(API_ROOT + "/sentiment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ quotes: quotes }),
    })
      .then(handleResponse)
      .then(renderAnalysis)
      .catch(function (error) {
        console.log(error);
        document.getElementById("results_status").innerHTML =
          "Can't get sentiments now. Sorry :(";
      });
  }

  async function renderAnalysis(results) {
    for (result of Object.keys(results)) {
      document.getElementById(result).innerHTML = results[result];
    }
    document.getElementById("results").style.display = "block";
    document.getElementById("results_status").innerHTML = "";
  }

  return {
    getAndAnalyzeQuotes: getAndAnalyzeQuotes,
  };
}

let kanye_client = KanyeClient();
