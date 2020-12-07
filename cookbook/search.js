//This file is for client-side searching

var savedContents;

window.onload = function() {
	var searchTerm = document.getElementsByClassName("search")[0].value = "";
}

function search(event) {
	//console.log(event.key);
	var searchTerm = document.getElementsByClassName("search")[0].value;
	//console.log(searchTerm);
	var results = searchResults(searchTerm);
	var holder;
	if (document.getElementsByClassName("normal-body-header-container").length === 0) {
		//document is a navigation page
		holder = document.getElementsByClassName("body-header-container")[0];
	} else {
		//document is normal text page
		holder = document.getElementsByClassName("normal-body-header-container")[0];
	}
	if (savedContents === undefined) {
		savedContents = holder.innerHTML;
	}
	if (searchTerm === "") {
		console.log("search term removed, reverting page");
		holder.innerHTML = savedContents;
	} else {
		holder.innerHTML = "";
		holder.innerHTML += "<h2 class=\"bodyheader\">Search Results</h2>";
		for (var i = 0; i < Math.min(results.length, 10); i++) {
			holder.innerHTML += "<a href="+pageDescriptions[results[i][0]][1]+"><p>"+pageDescriptions[results[i][0]][0]+"</p></a>"
		}
	}
}

var pageDescriptions = [['Hints and Suggestions', 'hints.html', 10], ["Ann's Crab Dip", 'annCrabDip.html', 3], ['Baklazhannaia Ikra', 'baklazhannaia.html', 5], ["Aunt Beth's Crab Dip", 'bethCrabDip.html', 4], ['Broiled Clams', 'broiledClams.html', 4], ['Buffalo Chicken Dip', 'buffaloDip.html', 3], ['Caponata', 'caponata.html', 1], ['Crabbies', 'crabbies.html', 1], ['Sausage Cheese Balls', 'sausageCheeseBalls.html', 3], ['Stuffed Cucumber', 'stuffedCucumber.html', 2], ['Vegetable Dip', 'vegetableDip.html', 2], ['Appetizers', 'appetizers.html', 1], ['Banana Bread', 'bananaBread.html', 2], ['Biscuits', 'biscuitsRecipe.html', 1], ["Bishop's Bread", 'bishopBread.html', 2], ['Blueberry Coffee Cake', 'blueberryCoffeeCake.html', 3], ['Buttermilk Hotcakes', 'buttermilkHotcakes.html', 2], ['Chippewa Fried Bread', 'chippewaFriedBread.html', 3], ['Cornmeal Mush', 'cornmealMush.html', 2], ['Crunchy Gradnola', 'crunchyGradnola.html', 2], ['Dutch Babies', 'dutchBabies.html', 2], ['Funnel Cakes', 'funnelCakes.html', 2], ['Gingerbread Scones', 'gingerbreadScones.html', 2], ['Northern Sweet Cornbread', 'northernSweetCornbread.html', 3], ['Pumpkin Nut Bread', 'pumpkinNutBread.html', 3], ['Sour-Cream Coffee Cake', 'sourCreamCoffeeCake.html', 3], ['Tea Scones', 'teaScones.html', 2], ['Waffles', 'waffles.html', 1], ['Biscuits, Breakfast, and Batter Breads', 'biscuits.html', 5], ['Austrian Striezel', 'austrianStriezel.html', 7], ['French Bread', 'frenchBread.html', 2], ['Hamburger Buns', 'hamburgerBuns.html', 4], ['Hot Cross Buns', 'hotCrossBuns.html', 3], ["Hulda's Rolls", 'huldaRoll.html', 2], ['Lucia Cats', 'luciaCats.html', 4], ['Monkey Bread', 'monkeyBread.html', 2], ['Nova Scotia Bread', 'novaScotiaBread.html', 3], ['Pizza', 'pizza.html', 1], ['Portuguese Bread', 'portugueseBread.html', 2], ['Rolls', 'rolls.html', 1], ['Steamed Buns', 'steamedBuns.html', 2], ['Bread, Rolls and Buns', 'bread.html', 4], ['Seven Layer Cookies', '7LayerCookies.html', 3], ['Angel Food Cake', 'angelFoodCake.html', 3], ['Applesauce Cookies', 'applesauceCookies.html', 2], ['Baklava', 'baklava.html', 1], ['Berry Pie', 'berryPie.html', 2], ['Bourbon Balls', 'bourbonBalls.html', 2], ['Braunes Lebkuchen Cookies', 'braunesLebkuchen.html', 3], ['Buttermilk Icing', 'buttermilkIcing.html', 2], ['Candy Cane Cookies', 'candyCaneCookies.html', 3], ['Carmel Icing', 'carmelIcing.html', 2], ['Carrot Cookies', 'carrotCookies.html', 2], ['Cheescake', 'cheesecake.html', 1], ['Chinese Almond Cookies', 'chineseAlmondCookies.html', 3], ['Chocolate Cake', 'chocolateCake.html', 2], ['Chocolate Icing', 'chocolateIcing.html', 2], ['Cinnamon/Sugar Goodies', 'cinnamonGoodies.html', 2], ['Cioccolato Paradiso', 'cioccolatoParadiso.html', 3], ['Citrus Poppy-Seed Cake', 'citrusPoppyCake.html', 3], ['Shiny Cream-Cheese Frosting', 'creamCheeseFrosting.html', 3], ['Lemon Glaze', 'lemonGlaze.html', 2], ['Citrus Poppy-Seed Cake (Entire Recipe)', 'citrusPoppyCakeRecipe.html', 5], ['Cowboy Cookies', 'cowboyCookies.html', 2], ['Creamy Rice Pudding', 'creamyRicePudding.html', 3], ["Devil's Food Cake", 'devilFoodCake.html', 3], ['Sugar Cookies (Edith)', 'edithSugarCookies.html', 3], ['English Toffee', 'englishToffee.html', 2], ['Festive Date Fills', 'festiveDateFills.html', 3], ['Fudge', 'fudge.html', 1], ['Coconut Pecan Frosting', 'coconutPecanFrosting.html', 3], ['German Sweet Chocolate Cake', 'germanSweetChocolateCake.html', 4], ['German Sweet Chocolate Cake (Folder)', 'germanChocolateCakeRecipe.html', 5], ['Gingerbread', 'gingerbread.html', 1], ["Grannie's Oat Cakes", 'grannieOatCake.html', 3], ['Granny Cake', 'grannyCake.html', 4], ["Hulda's Dessert", 'huldaDessert.html', 2], ['Kentucky Jam Cake', 'kentuckyJamCake.html', 3], ['Lemon Bars', 'lemonBars.html', 2], ['Lemon Cake', 'lemonCake.html', 2], ["Mom's Pie Crust", 'momPieCrust.html', 3], ['Monster Cookies', 'monsterCookies.html', 2], ['No-Cook Chocolate Frosting', 'noCookChocolateFrosting.html', 3], ['Oatmeal Cake', 'oatmealCake.html', 2], ['Oatmeal Chocolate Chip Cookies', 'oatmealChocolateChipCookies.html', 4], ['Petits Pains Au Chocolat', 'painsAuChocolat.html', 4], ['Peanut Brittle', 'peanutBrittle.html', 2], ['Peanut Butter Cookies', 'peanutButterCookies.html', 3], ['Pecan Tassies', 'pecanTassies.html', 2], ['Pfeffernuesse', 'pfeffernuesse.html', 3], ['Pumpkin Bars', 'pumpkinBar.html', 2], ['Pumpkin Pie', 'pumpkinPie.html', 2], ['Sliced Lemon Pie', 'slicedLemonPie.html', 3], ['Springerli', 'springerli.html', 1], ['Steamed Rice Cake', 'steamedRiceCake.html', 3], ['Stuffed Date Cookies', 'stuffedDateCookies.html', 3], ['Sugar Cookies', 'sugarCookies.html', 2], ['P\xc3\xa2te Sucr\xc3\xa9e Plaza-Ath\xc3\xa9n\xc3\xa9e', 'pateSucree.html', 3], ['Sweet Almond Butter', 'sweetAlmondButter.html', 6], ['Tart Auz Airelles Plaza-Ath\xc3\xa9n\xc3\xa9e', 'tartAuxAirelles.html', 6], ['Tart Auz Airelles Plaza-Ath\xc3\xa9n\xc3\xa9e (Folder)', 'tartAuxRecipe.html', 5], ['Thunder Cake', 'thunderCake.html', 2], ['Vanilla Ice Cream', 'vanillaIceCream.html', 3], ['Zucchini Cake', 'zucchiniCake.html', 2], ['Desserts', 'desserts.html', 1], ['Cocoa Mix', 'cocoa.html', 2], ['PERFECT MARTINI', 'martini.html', 2], ['Polish Vodka', 'polishVodka.html', 2], ['Drinks', 'drinks.html', 1], ['All In One Family', 'allInOneFamily.html', 4], ['Apricot Chicken', 'apricotChicken.html', 2], ['Baked Whitefish', 'bakedWhitefish.html', 2], ['Baked Ziti', 'bakedZiti.html', 2], ['Beef Stroganoff', 'beefStroganov.html', 2], ['Beef Sukiyaki', 'beefSukiyaki.html', 2], ['BOEUF BOURGUIGNON', 'boeufBourguignon.html', 2], ['Cauloflower Cheese Pie', 'cauliflowerCheesePie.html', 8], ['Chicken Bouillabase', 'chickenBouillabase.html', 2], ['Chinese Pork Roast', 'chinesePorkRoast.html', 3], ['Clam Chowder', 'clamChowder.html', 2], ['Clam Fritters', 'clamFritters.html', 2], ['Clam And Oyster Pie', 'classOysterPie.html', 4], ['Coquilles', 'coquilles.html', 4], ['Crab And Spinach Casserole', 'crabAndSpinachCasserole.html', 4], ['Easy Moist Chicken', 'easyMoistChicken.html', 3], ['Feijoda', 'feijoda.html', 2], ['Fish Cakes', 'fishCakes.html', 2], ['Four-In-Hand Chicken', 'fourInHandChicken.html', 2], ['Fried Chicken', 'friedChicken.html', 2], ['Fried Combination Rice', 'friedCombinationRice.html', 3], ['Fried Ketchup Shrimp', 'friedKetchupShrimp.html', 3], ['Fried Rice', 'friedRice.html', 2], ['Ham Loaf', 'hamLoaf.html', 2], ['Ham Spread', 'hamSpread.html', 2], ['Kenyan Curry And Fish', 'kenyanCurryFish.html', 4], ['KULEBIAKA', 'kulebiaka.html', 1], ['Lamb And Tahini-Stuffed Pita Wedges', 'lambPitaWedges.html', 5], ['Lasagne', 'lasagne.html', 1], ['Chicken With Lemon and Herbs', 'lemonAndHerbChicken.html', 5], ['Malaysian Steamboat', 'malaysianSteamboat.html', 2], ['Marinated Chicken Breast', 'marinatedChickenBreasts.html', 3], ['Meatloaf', 'meatloaf.html', 1], ['More', 'more.html', 1], ['Moussaka', 'moussaka.html', 1], ['Mussels In A Light Italian Sauce', 'musselsInSauce.html', 6], ['One Pot Meal', 'onePotMean.html', 3], ['Pasta With Clam And Vegitable Sauce', 'pastaWithClamSauce.html', 6], ['Pizza A La Pickens', 'pizzaALaPickens.html', 4], ['Pork Loaf', 'porkLoaf.html', 2], ['Quiche', 'quiche.html', 1], ['Refried Beans - New Mexican Style', 'refriedBeans.html', 6], ['Salmon In Cork Husk Boats', 'salmonInCork.html', 5], ['Satay', 'satay.html', 1], ['Shirred Eggs', 'shirredEggs.html', 2], ['SHRIMP ETOUFF\xc3\x89E', 'shrimpEtouffee.html', 2], ['Singapore Noodles', 'singaporeNoodles.html', 2], ['Steak And Okra Gumbo', 'steakAndOkraGumbo.html', 4], ['Steamed Fish', 'steamedFish.html', 2], ['Sweet And Sour Fish', 'sweetAndSourFish.html', 4], ['Sweet And Sour Shrimp', 'sweetSourShrimp.html', 4], ['Swiss Fondue', 'swissFondue.html', 2], ['Tempura', 'tempura.html', 1], ['Texas Red Chili', 'texasRedChili.html', 3], ['Turkey CR\xc3\x8aPES', 'turkeyCrepes.html', 2], ['Turkey Tetrazini', 'turkeyTetrazini.html', 2], ['Turkey Wraps', 'turkeyWraps.html', 7], ['Veal Parmesan', 'vealParmesan.html', 2], ["Venus' Belly Button", 'venusBellyButton.html', 3], ['Entrees', 'entrees.html', 1], ['Apple Butter', 'appleButter.html', 2], ['Berry Jam', 'berryJam.html', 2], ['Lemon Curd', 'lemonCurd.html', 2], ['Jams And Jellies', 'jamsAndJellies.html', 3], ["Brisco's Chili Picosa", 'chiliPicosa.html', 3], ['Kraut Relish', 'krautRelish.html', 2], ['Pickled Ginger', 'pickledGinger.html', 2], ['Pickles And Relishes', 'picklesRelishes.html', 3], ['Black Bean And Corn Salad', 'blackBeanCornSalad.html', 5], ['Cauliflower Salad', 'cauliflowerSalad.html', 2], ['Celery Seed Dressing', 'celerySeedDressing.html', 6], ['Cranberry Salad', 'cranberrySalad.html', 2], ['Danish Potato Salad', 'danishPotatoSalad.html', 3], ['GREEN BEAN, RED ONION, AND ROAST POTATO SALAD', 'greenBeanSalad.html', 11], ['Kale and Brussels Sprout Salad', 'kaleBrusselsSalad.html', 5], ["Lilian's Salad", 'liliansSalad.html', 2], ['MINTED GREEN BEANS WITH RED ONION', 'mintedGreenBeans.html', 6], ["Paula Wengerd's Salads", 'paulasSalads.html', 3], ['Pickled Cucumber Salad', 'pickledCucumberSalad.html', 3], ['Salad Dressing', 'saladDressing.html', 2], ['PARMESAN WALNUT SALAD IN ENDIVE LEAVES', 'walnutSalad.html', 6], ['Salads', 'salads.html', 1], ['Red Eye Gravy', 'redEyeGravy.html', 3], ['Spaghetti Sauce', 'spaghettiSauce.html', 2], ['White Gravy', 'whiteGravy.html', 2], ['Sauces And Gravies', 'sauces.html', 3], ['Baked Beans', 'bakedBeans.html', 2], ['PAUL PRUDOMME\xe2\x80\x99S BASIC RICE', 'basicRice.html', 4], ['BROWN RICE SALAD WITH MANGO CHUTNEY DRESSING', 'brownRiceSalad.html', 7], ['Cabbage', 'cabbage.html', 1], ['Chippewa Wild Rice', 'chippewaWildRice.html', 3], ['CHESAPEAKE BAY ISLAND CORN PUDDING', 'cornPudding.html', 5], ['COWPOKE BEANS', 'cowpokeBeans.html', 2], ['GREEN BEANS WITH ROASTED VEGETABLES', 'greenBeans.html', 5], ["Laurie's Potatoes", 'lauriesPotatoes.html', 2], ['Ratatouille', 'ratatouille.html', 1], ['Roasted Vegetables', 'roastedVegetables.html', 6], ['Spinach Ring', 'spinachRing.html', 2], ['Stuffed Tomatoes', 'stuffedTomatoes.html', 2], ['Side Dishes', 'sideDishes.html', 2], ['Barley And Lentil Soup', 'barleyLentilSoup.html', 7], ['Broccoli Soup', 'broccoliSoup.html', 2], ['FABIO\xe2\x80\x99S CREAMY CREAMLESS SQUASH SOUP', 'creamySquashSoup.html', 5], ["ROSE'S ESCAROLE SOUP", 'escaroleSoup.html', 3], ['Leek And Potato Soup', 'leekAndPotatoSoup.html', 4], ['Minestrone', 'minestone.html', 1], ['Oxtain Ragout', 'oxtailRagout.html', 2], ['Puree Mongole', 'pureeMongole.html', 2], ['Tomato Soup', 'tomatoSoup.html', 4], ['Soups', 'soups.html', 1], ['Recipes', 'index.html', 1], ['Introduction', 'introduction.html', 1]];
var searchTerms = [["hints,", 0],["suggestions,", 0],["reminders", 0],["and", 0],["other", 0],["things", 0],["you", 0],["have", 0],["heard", 0],["before", 0],["ann's", 1],["crab", 1],["dip", 1],["baklazhannaia", 2],["ikra", 2],["(poor", 2],["man's", 2],["caviar)", 2],["aunt", 3],["beth's", 3],["crab", 3],["dip", 3],["broiled", 4],["clams", 4],["and", 4],["oysters", 4],["buffalo", 5],["chicken", 5],["dip", 5],["caponata", 6],["crabbies", 7],["sausage", 8],["cheese", 8],["balls", 8],["stuffed", 9],["cucumber", 9],["vegetable", 10],["dip", 10],["appetizers", 11],["banana", 12],["bread", 12],["biscuits", 13],["bishop's", 14],["bread", 14],["blueberry", 15],["coffee", 15],["cake", 15],["buttermilk", 16],["hotcakes", 16],["chippewa", 17],["fried", 17],["bread", 17],["cornmeal", 18],["mush", 18],["crunchy", 19],["gradnola", 19],["dutch", 20],["babies", 20],["funnel", 21],["cakes", 21],["gingerbread", 22],["scones", 22],["northern", 23],["sweet", 23],["cornbread", 23],["pumpkin", 24],["nut", 24],["bread", 24],["sour-cream", 25],["coffee", 25],["cake", 25],["tea", 26],["scones", 26],["waffles", 27],["biscuits,", 28],["breakfast,", 28],["and", 28],["batter", 28],["breads", 28],["austrian", 29],["striezel", 29],["(a.k.a.", 29],["christmas", 29],["and", 29],["easter", 29],["bread)", 29],["french", 30],["bread", 30],["hamburger", 31],["buns", 31],["(italian", 31],["rolls)", 31],["hot", 32],["cross", 32],["buns", 32],["hulda's", 33],["rolls", 33],["lucia", 34],["cats", 34],["(swedish", 34],["lussekatter)", 34],["monkey", 35],["bread", 35],["nova", 36],["scotia", 36],["bread", 36],["pizza", 37],["portuguese", 38],["bread", 38],["rolls", 39],["steamed", 40],["buns", 40],["bread,", 41],["rolls", 41],["and", 41],["buns", 41],["seven", 42],["layer", 42],["cookies", 42],["angel", 43],["food", 43],["cake", 43],["applesauce", 44],["cookies", 44],["baklava", 45],["berry", 46],["pie", 46],["bourbon", 47],["balls", 47],["braunes", 48],["lebkuchen", 48],["cookies", 48],["buttermilk", 49],["icing", 49],["candy", 50],["cane", 50],["cookies", 50],["carmel", 51],["icing", 51],["carrot", 52],["cookies", 52],["cheescake", 53],["chinese", 54],["almond", 54],["cookies", 54],["chocolate", 55],["cake", 55],["chocolate", 56],["icing", 56],["cinnamon/sugar", 57],["goodies", 57],["cioccolato", 58],["paradiso", 58],["(biscotti)", 58],["citrus", 59],["poppy-seed", 59],["cake", 59],["shiny", 60],["cream-cheese", 60],["frosting", 60],["lemon", 61],["glaze", 61],["citrus", 62],["poppy-seed", 62],["cake", 62],["(entire", 62],["recipe)", 62],["cowboy", 63],["cookies", 63],["creamy", 64],["rice", 64],["pudding", 64],["devil's", 65],["food", 65],["cake", 65],["sugar", 66],["cookies", 66],["(edith)", 66],["english", 67],["toffee", 67],["festive", 68],["date", 68],["fills", 68],["fudge", 69],["coconut", 70],["pecan", 70],["frosting", 70],["german", 71],["sweet", 71],["chocolate", 71],["cake", 71],["german", 72],["sweet", 72],["chocolate", 72],["cake", 72],["(folder)", 72],["gingerbread", 73],["grannie's", 74],["oat", 74],["cakes", 74],["granny", 75],["cake", 75],["(fudge", 75],["shortcake)", 75],["hulda's", 76],["dessert", 76],["kentucky", 77],["jam", 77],["cake", 77],["lemon", 78],["bars", 78],["lemon", 79],["cake", 79],["mom's", 80],["pie", 80],["crust", 80],["monster", 81],["cookies", 81],["no-cook", 82],["chocolate", 82],["frosting", 82],["oatmeal", 83],["cake", 83],["oatmeal", 84],["chocolate", 84],["chip", 84],["cookies", 84],["petits", 85],["pains", 85],["au", 85],["chocolat", 85],["peanut", 86],["brittle", 86],["peanut", 87],["butter", 87],["cookies", 87],["pecan", 88],["tassies", 88],["pfeffernuesse", 89],["(pepper", 89],["nuts)", 89],["pumpkin", 90],["bars", 90],["pumpkin", 91],["pie", 91],["sliced", 92],["lemon", 92],["pie", 92],["springerli", 93],["steamed", 94],["rice", 94],["cake", 94],["stuffed", 95],["date", 95],["cookies", 95],["sugar", 96],["cookies", 96],["pâte", 97],["sucrée", 97],["plaza-athénée", 97],["crème", 98],["d'amandes", 98],["plaza-athénée", 98],["(sweet", 98],["almond", 98],["butter)", 98],["tart", 99],["auz", 99],["airelles", 99],["plaza-athénée", 99],["(cranberry", 99],["tart)", 99],["tart", 100],["auz", 100],["airelles", 100],["plaza-athénée", 100],["(folder)", 100],["thunder", 101],["cake", 101],["vanilla", 102],["ice", 102],["cream", 102],["zucchini", 103],["cake", 103],["desserts", 104],["cocoa", 105],["mix", 105],["perfect", 106],["martini", 106],["polish", 107],["vodka", 107],["drinks", 108],["all", 109],["in", 109],["one", 109],["family", 109],["apricot", 110],["chicken", 110],["baked", 111],["whitefish", 111],["baked", 112],["ziti", 112],["beef", 113],["stroganoff", 113],["beef", 114],["sukiyaki", 114],["boeuf", 115],["bourguignon", 115],["cauloflower", 116],["cheese", 116],["pie", 116],["-", 116],["with", 116],["grated", 116],["potato", 116],["crust", 116],["chicken", 117],["bouillabase", 117],["chinese", 118],["pork", 118],["roast", 118],["clam", 119],["chowder", 119],["clam", 120],["fritters", 120],["clam", 121],["and", 121],["oyster", 121],["pie", 121],["coquilles", 122],["st.", 122],["jacques", 122],["baumaniÉre", 122],["crab", 123],["and", 123],["spinach", 123],["casserole", 123],["easy", 124],["moist", 124],["chicken", 124],["feijoada", 125],["(fai-zho-ah-da)", 125],["fish", 126],["cakes", 126],["four-in-hand", 127],["chicken", 127],["fried", 128],["chicken", 128],["fried", 129],["combination", 129],["rice", 129],["fried", 130],["ketchup", 130],["shrimp", 130],["fried", 131],["rice", 131],["ham", 132],["loaf", 132],["ham", 133],["spread", 133],["kenyan", 134],["curry", 134],["and", 134],["fish", 134],["kulebiaka", 135],["lamb", 136],["and", 136],["tahini-stuffed", 136],["pita", 136],["wedges", 136],["lasagne", 137],["chicken", 138],["with", 138],["lemon", 138],["and", 138],["herbs", 138],["malaysian", 139],["steamboat", 139],["marinated", 140],["chicken", 140],["breast", 140],["meatloaf", 141],["more", 142],["moussaka", 143],["mussels", 144],["in", 144],["a", 144],["light", 144],["italian", 144],["sauce", 144],["one", 145],["pot", 145],["meal", 145],["pasta", 146],["with", 146],["clam", 146],["and", 146],["vegitable", 146],["sauce", 146],["pizza", 147],["a", 147],["la", 147],["pickens", 147],["pork", 148],["loaf", 148],["quiche", 149],["refried", 150],["beans", 150],["-", 150],["new", 150],["mexican", 150],["style", 150],["salmon", 151],["in", 151],["cork", 151],["husk", 151],["boats", 151],["satay", 152],["shirred", 153],["eggs", 153],["shrimp", 154],["etouffÉe", 154],["singapore", 155],["noodles", 155],["steak", 156],["and", 156],["okra", 156],["gumbo", 156],["steamed", 157],["fish", 157],["sweet", 158],["and", 158],["sour", 158],["fish", 158],["sweet", 159],["and", 159],["sour", 159],["shrimp", 159],["swiss", 160],["fondue", 160],["tempura", 161],["texas", 162],["red", 162],["chili", 162],["turkey", 163],["crÊpes", 163],["turkey", 164],["tetrazini", 164],["turkey", 165],["wraps", 165],["with", 165],["curry-chutney", 165],["mayonnaise", 165],["and", 165],["peanuts", 165],["veal", 166],["parmesan", 166],["venus'", 167],["belly", 167],["button", 167],["entrees", 168],["apple", 169],["butter", 169],["berry", 170],["jam", 170],["lemon", 171],["curd", 171],["jams", 172],["and", 172],["jellies", 172],["brisco's", 173],["chili", 173],["picosa", 173],["kraut", 174],["relish", 174],["pickled", 175],["ginger", 175],["pickles", 176],["and", 176],["relishes", 176],["black", 177],["bean", 177],["and", 177],["corn", 177],["salad", 177],["cauliflower", 178],["salad", 178],["celery", 179],["seed", 179],["dressing", 179],["for", 179],["fruit", 179],["salad", 179],["cranberry", 180],["salad", 180],["danish", 181],["potato", 181],["salad", 181],["green", 182],["bean,", 182],["red", 182],["onion,", 182],["and", 182],["roast", 182],["potato", 182],["salad", 182],["with", 182],["rosemary", 182],["vinaigrette", 182],["kale", 183],["and", 183],["brussels", 183],["sprout", 183],["salad", 183],["lilian's", 184],["salad", 184],["minted", 185],["green", 185],["beans", 185],["with", 185],["red", 185],["onion", 185],["paula", 186],["wengerd's", 186],["salads", 186],["pickled", 187],["cucumber", 187],["salad", 187],["salad", 188],["dressing", 188],["parmesan", 189],["walnut", 189],["salad", 189],["in", 189],["endive", 189],["leaves", 189],["salads", 190],["red", 191],["eye", 191],["gravy", 191],["spaghetti", 192],["sauce", 192],["white", 193],["gravy", 193],["sauces", 194],["and", 194],["gravies", 194],["baked", 195],["beans", 195],["paul", 196],["prudomme’s", 196],["basic", 196],["rice", 196],["brown", 197],["rice", 197],["salad", 197],["with", 197],["mango", 197],["chutney", 197],["dressing", 197],["cabbage", 198],["chippewa", 199],["wild", 199],["rice", 199],["chesapeake", 200],["bay", 200],["island", 200],["corn", 200],["pudding", 200],["cowpoke", 201],["beans", 201],["green", 202],["beans", 202],["with", 202],["roasted", 202],["vegetables", 202],["laurie's", 203],["potatoes", 203],["ratatouille", 204],["oven-roasted", 205],["spring", 205],["vegetables", 205],["with", 205],["salsa", 205],["verde", 205],["spinach", 206],["ring", 206],["stuffed", 207],["tomatoes", 207],["side", 208],["dishes", 208],["barley", 209],["and", 209],["lentil", 209],["soup", 209],["with", 209],["swiss", 209],["chard", 209],["broccoli", 210],["soup", 210],["fabio’s", 211],["creamy", 211],["creamless", 211],["squash", 211],["soup", 211],["rose's", 212],["escarole", 212],["soup", 212],["leek", 213],["and", 213],["potato", 213],["soup", 213],["minestrone", 214],["oxtain", 215],["ragout", 215],["puree", 216],["mongole", 216],["tomato", 217],["soup", 217],["florentine", 217],["style", 217],["soups", 218],["recipes", 219],["introduction", 220]];


function searchResults(term) {
	term = term.toLocaleLowerCase().split(" ");
	var res = [];
	//[address, index]
	for (var i = 0; i < term.length; i++) {
		for (var j = 0; j < searchTerms.length; j++) {
			//console.log("Comparing "+term[i]+" and "+searchTerms[j][0]);
			var n = searchIndex(term[i], searchTerms[j][0]) / pageDescriptions[searchTerms[j][1]][2];
			//console.log("\tThey got a score of: "+n);
			if (n > 0) {
				var found = false;
				for (var k = 0; k < res.length; k++) {
					if (res[k][0] === searchTerms[j][1]) {
						found = true;
						//console.log("\t\texisting entry exists, adding");
						res[k][1]+=n;
						break;
					}
				}
				if (!found) {
					//console.log("\t\texisting entry not found, adding entry");
					res.push([searchTerms[j][1], n]);
				}
			}
		}
	}
	function compare(a, b) {
		if (a[1] < b[1]) {
			return -1;
		}
		if (a[1] > b[1]) {
			return 1;
		}
		return 0;
	}
	return res.sort(compare).reverse();
}

function searchIndex(a, b) {
	var small, large;
	if (a.length > b.length) {
		large = a;
		small = b;
	} else {
		large = b;
		small = a;
	}

	var testN = small.length + large.length - 1;
	var maxMatch = 0;
	for (var i = 0; i < testN; i++) {
		var minI = Math.max(0, i - small.length + 1);
		var maxI = Math.min(large.length, i+1);
		var matches = 0;
		for (var j = minI; j < maxI; j++) {
			//console.log("\t\tcomparing " + small[j-i+small.length-1] + " and " + large[j]);
			if (small[j-i+small.length-1] === large[j]) {
				matches++;
			}
		}
		//console.log("found "+matches+" matches");
		maxMatch = Math.max(maxMatch, matches);
	}
	//console.log("Max matches: "+maxMatch);
	//console.log("result: "+maxMatch / small.length)
	if (large.length === 0) {
		return 0;
	}
	return maxMatch / large.length;
}

function printRecipe() {
	console.log("printing");
	var wholePage = document.body.innerHTML;
	var holder;
	if (document.getElementsByClassName("normal-body-header-container").length === 0) {
		//document is a navigation page
		holder = document.getElementsByClassName("body-header-container")[0];
	} else {
		//document is normal text page
		holder = document.getElementsByClassName("normal-body-header-container")[0];
	}

	document.body.innerHTML = holder.innerHTML;
	document.body.removeChild(document.body.firstElementChild)

	window.print();

	document.body.innerHTML = wholePage;
}