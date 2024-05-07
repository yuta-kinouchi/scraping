function scrapeSuumoPagesWithPhantomJsCloud() {
  // PhantomJsCloudのAPI設定
  let key =
    PropertiesService.getScriptProperties().getProperty("PHANTOMJSCLOUD_ID");
  var phantomJsCloudUrl = `https://phantomjscloud.com/api/browser/v2/${key}/`;

  // ベースURLと最大ページ数の設定
  var baseUrl = "https://suumo.jp";
  var url = "https://suumo.jp/chintai/tokyo/ek_27280/";
  var maxPages = 10;

  // スプレッドシートの準備
  var spreadsheetId = "1LkPfM_8mdFGL3qYNbF-I5rkYqkiNpWo28PI4-1RcKek";
  var sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();
  sheet.clear();
  sheet.appendRow([
    "物件名",
    "住所",
    "駅徒歩",
    "築年数",
    "階数",
    "賃料",
    "敷金",
    "礼金",
    "間取り",
    "専有面積（平方メートル）",
  ]);

  // 現在のページとURLの初期化
  var currentPage = 1;
  while (currentPage <= maxPages) {
    // PhantomJsCloud APIリクエストの作成
    var requestBody = {
      url: url,
      renderType: "html",
      outputAsJson: false,
    };

    // PhantomJsCloud APIへのリクエスト送信
    var response = UrlFetchApp.fetch(phantomJsCloudUrl, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(requestBody),
      muteHttpExceptions: true,
    });

    // レスポンスのHTMLを取得
    var responseBody = response.getContentText();

    // 各種フィールドの正規表現と配列の定義
    var titlesRegex = /<div class="cassetteitem_content-title">(.*?)<\/div>/g;
    var addressRegex = /<li class="cassetteitem_detail-col1">(.*?)<\/li>/g;
    var walkFromStationRegex =
      /<div class="cassetteitem_detail-text">(.*?)<\/div>/g;
    var ageAndFloorRegex =
      /<li class="cassetteitem_detail-col3">\s*<div>(.*?)<\/div>\s*<div>(.*?)<\/div>/g;
    var pricesRegex =
      /<span class="cassetteitem_other-emphasis ui-text--bold">(.*?)<\/span>/g;
    var securityDepositRegex =
      /<span class="cassetteitem_price cassetteitem_price--deposit">(.*?)<\/span>/g;
    var keyMoneyRegex =
      /<span class="cassetteitem_price cassetteitem_price--gratuity">(.*?)<\/span>/g;
    var floorPlanRegex = /<span class="cassetteitem_madori">(.*?)<\/span>/g;
    var areaRegex = /<span class="cassetteitem_menseki">(.*?)<\/span>/g;

    // 各項目の抽出結果を格納する配列
    var titles = [],
      addresses = [],
      walks = [],
      ages = [],
      floors = [],
      prices = [],
      deposits = [],
      keyMoneys = [],
      plans = [],
      areas = [];

    // 正規表現を使って各フィールドのデータを抽出
    var titleMatch,
      addressMatch,
      walkMatch,
      ageMatch,
      floorMatch,
      priceMatch,
      depositMatch,
      keyMoneyMatch,
      planMatch,
      areaMatch;

    while ((titleMatch = titlesRegex.exec(responseBody)) !== null) {
      titles.push(titleMatch[1].trim());
    }
    while ((addressMatch = addressRegex.exec(responseBody)) !== null) {
      addresses.push(addressMatch[1].trim());
    }
    while ((walkMatch = walkFromStationRegex.exec(responseBody)) !== null) {
      walks.push(walkMatch[1].trim());
    }
    while ((match = ageAndFloorRegex.exec(responseBody)) !== null) {
      ages.push(match[1].trim());
      floors.push(match[2].trim());
    }
    while ((priceMatch = pricesRegex.exec(responseBody)) !== null) {
      prices.push(priceMatch[1].trim());
    }
    while ((depositMatch = securityDepositRegex.exec(responseBody)) !== null) {
      deposits.push(depositMatch[1].trim());
    }
    while ((keyMoneyMatch = keyMoneyRegex.exec(responseBody)) !== null) {
      keyMoneys.push(keyMoneyMatch[1].trim());
    }
    while ((planMatch = floorPlanRegex.exec(responseBody)) !== null) {
      plans.push(planMatch[1].trim());
    }
    while ((areaMatch = areaRegex.exec(responseBody)) !== null) {
      var numberRegex = /([\d.]+)m<sup>/;
      var match = numberRegex.exec(areaMatch);
      var area = match ? match[1] : null;
      areas.push(area);
    }

    // 各項目のデータをスプレッドシートに書き込む
    for (var i = 0; i < titles.length; i++) {
      if (
        titles[i] &&
        addresses[i] &&
        walks[i] &&
        ages[i] &&
        floors[i] &&
        prices[i] &&
        deposits[i] &&
        keyMoneys[i] &&
        plans[i] &&
        areas[i]
      ) {
        sheet.appendRow([
          titles[i],
          addresses[i],
          walks[i],
          ages[i],
          floors[i],
          prices[i],
          deposits[i],
          keyMoneys[i],
          plans[i],
          areas[i],
        ]);
      }
    }

    // 「次へ」リンクの検索
    var nextPageRegex = /<a.*?href="([^"]*?)".*?>次へ<\/a>/;
    var nextPageMatch = nextPageRegex.exec(responseBody);

    if (nextPageMatch && currentPage < maxPages) {
      url = baseUrl + nextPageMatch[1]; // 次のページのURLを生成
      currentPage++;
    } else {
      break; // 次のページがないか、最大ページ数に達したら終了
    }
  }
}
