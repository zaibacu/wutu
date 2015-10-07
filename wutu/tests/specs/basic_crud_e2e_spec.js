describe("Basic CRUD operation from front-end", function(){
	beforeEach(function(){
		browser.get("http://localhost:5555");
	});

	it("should let you to add note", function(){
		var note = element(by.model("note.text"));
		note.sendKeys("tempnote");
		note.submit();

		var note = element(by.xpath("//span[text() = 'tempnote']"));
		expect(note.isPresent()).toBe(true);
	});

	it("should let you delete selected note", function(){
		var delButton = element(by.xpath("//span[text() = 'tempnote']")).element(by.xpath("../button"));
		delButton.click();

		var note = element(by.xpath("//span[text() = 'tempnote']"));
		expect(note.isPresent()).toBe(false);
	});
});