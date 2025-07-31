if __name__ == "__main__":
    from app import create_analysis_prompt, analyze_with_llm, format_response
    prompt = create_analysis_prompt('hello, I am a ML engineer', 'hello, we need a ML engineer') 
    print("Prompt:", prompt)
    print("\n" + "="*50)
    
    analysis = analyze_with_llm('hello, I am a ML engineer', 'hello, we need a ML engineer')
    print("Analysis result:")
    print(f"Match percentage: {analysis.get('match_percentage', 'N/A')}")
    print(f"Strengths: {analysis.get('strengths', [])}")
    print(f"Weaknesses: {analysis.get('weaknesses', [])}")
    print(f"Suggestions: {analysis.get('suggestions', [])}")
    print(f"Is fallback: {analysis.get('is_fallback', 'N/A')}")
    print(f"Fallback reason: {analysis.get('fallback_reason', 'N/A')}")
    
    # Test that is_fallback is always present
    assert 'is_fallback' in analysis, "is_fallback field should always be present"
    assert isinstance(analysis['is_fallback'], bool), "is_fallback should be a boolean"
    
    # Test that fallback_reason is present when fallback is used
    if analysis['is_fallback']:
        assert 'fallback_reason' in analysis, "fallback_reason should be present when fallback is used"
        assert isinstance(analysis['fallback_reason'], str), "fallback_reason should be a string"
        assert len(analysis['fallback_reason']) > 0, "fallback_reason should not be empty"
    
    print("\n✅ Test passed: Fallback indicator is properly implemented!")
    
    print("\n" + "="*50)
    print("Testing format_response method:")
    print("="*50)
    
    # Test 1: Well-structured LLM response
    test_response_1 = """
    The candidate has relevant experience and skills. Match: 85%. 
    Strengths: Technical background, relevant experience, good communication skills. 
    Weaknesses: Could use more specific examples, limited project management experience. 
    Suggestions: Add project examples, include certifications, highlight leadership roles.
    """
    
    result_1 = format_response(test_response_1)
    print(f"Test 1 - Well-structured response:")
    print(f"  Match: {result_1['match_percentage']}")
    print(f"  Strengths: {result_1['strengths']}")
    print(f"  Weaknesses: {result_1['weaknesses']}")
    print(f"  Suggestions: {result_1['suggestions']}")
    
    # Test 2: Response with different formatting
    test_response_2 = """
    Match: 70%
    Strengths: Python programming, machine learning, data analysis
    Weaknesses: No cloud experience, limited team leadership
    Suggestions: Learn AWS, take leadership courses, add more projects
    """
    
    result_2 = format_response(test_response_2)
    print(f"\nTest 2 - Different formatting:")
    print(f"  Match: {result_2['match_percentage']}")
    print(f"  Strengths: {result_2['strengths']}")
    print(f"  Weaknesses: {result_2['weaknesses']}")
    print(f"  Suggestions: {result_2['suggestions']}")
    
    # Test 3: Response with semicolon-separated lists
    test_response_3 = """
    The candidate matches 60%. 
    Strengths: Technical skills; problem solving; analytical thinking
    Weaknesses: Limited experience; communication skills need improvement
    Suggestions: Gain more experience; improve communication; add certifications
    """
    
    result_3 = format_response(test_response_3)
    print(f"\nTest 3 - Semicolon-separated:")
    print(f"  Match: {result_3['match_percentage']}")
    print(f"  Strengths: {result_3['strengths']}")
    print(f"  Weaknesses: {result_3['weaknesses']}")
    print(f"  Suggestions: {result_3['suggestions']}")
    
    # Test 4: Empty or minimal response
    test_response_4 = "The candidate is a good fit."
    result_4 = format_response(test_response_4)
    print(f"\nTest 4 - Minimal response:")
    print(f"  Match: {result_4['match_percentage']}")
    print(f"  Strengths: {result_4['strengths']}")
    print(f"  Weaknesses: {result_4['weaknesses']}")
    print(f"  Suggestions: {result_4['suggestions']}")
    
    # Test 5: Response with no match percentage
    test_response_5 = """
    Strengths: Good technical background
    Weaknesses: Limited experience
    Suggestions: Add more projects
    """
    
    result_5 = format_response(test_response_5)
    print(f"\nTest 5 - No match percentage:")
    print(f"  Match: {result_5['match_percentage']}")
    print(f"  Strengths: {result_5['strengths']}")
    print(f"  Weaknesses: {result_5['weaknesses']}")
    print(f"  Suggestions: {result_5['suggestions']}")
    
    # Assertions for format_response tests
    print("\n" + "="*50)
    print("Running assertions for format_response:")
    
    # Test 1 assertions
    assert result_1['match_percentage'] == '85', f"Expected '85', got {result_1['match_percentage']}"
    assert 'Technical background' in result_1['strengths'], "Should extract 'Technical background'"
    assert 'Could use more specific examples' in result_1['weaknesses'], "Should extract weakness"
    assert 'Add project examples' in result_1['suggestions'], "Should extract suggestion"
    
    # Test 2 assertions
    assert result_2['match_percentage'] == '70', f"Expected '70', got {result_2['match_percentage']}"
    assert 'Python programming' in result_2['strengths'], "Should extract 'Python programming'"
    assert 'No cloud experience' in result_2['weaknesses'], "Should extract weakness"
    assert 'Learn AWS' in result_2['suggestions'], "Should extract suggestion"
    
    # Test 3 assertions
    assert result_3['match_percentage'] == '60', f"Expected '60', got {result_3['match_percentage']}"
    assert 'Technical skills' in result_3['strengths'], "Should extract 'Technical skills'"
    assert 'Limited experience' in result_3['weaknesses'], "Should extract weakness"
    assert 'Gain more experience' in result_3['suggestions'], "Should extract suggestion"
    
    # Test 4 assertions (minimal response)
    assert result_4['match_percentage'] is None, "Should be None for minimal response"
    assert len(result_4['strengths']) == 0, "Should have empty strengths for minimal response"
    assert len(result_4['weaknesses']) == 0, "Should have empty weaknesses for minimal response"
    assert len(result_4['suggestions']) == 0, "Should have empty suggestions for minimal response"
    
    # Test 5 assertions (no match percentage)
    assert result_5['match_percentage'] is None, "Should be None when no match percentage found"
    assert 'Good technical background' in result_5['strengths'], "Should extract strength"
    assert 'Limited experience' in result_5['weaknesses'], "Should extract weakness"
    assert 'Add more projects' in result_5['suggestions'], "Should extract suggestion"
    
    # Test that all results have the expected structure
    for i, result in enumerate([result_1, result_2, result_3, result_4, result_5], 1):
        assert 'match_percentage' in result, f"Test {i}: Missing match_percentage"
        assert 'strengths' in result, f"Test {i}: Missing strengths"
        assert 'weaknesses' in result, f"Test {i}: Missing weaknesses"
        assert 'suggestions' in result, f"Test {i}: Missing suggestions"
        assert isinstance(result['strengths'], list), f"Test {i}: Strengths should be list"
        assert isinstance(result['weaknesses'], list), f"Test {i}: Weaknesses should be list"
        assert isinstance(result['suggestions'], list), f"Test {i}: Suggestions should be list"
        assert len(result['strengths']) <= 3, f"Test {i}: Strengths should be limited to 3"
        assert len(result['weaknesses']) <= 3, f"Test {i}: Weaknesses should be limited to 3"
        assert len(result['suggestions']) <= 3, f"Test {i}: Suggestions should be limited to 3"
    
    print("✅ All format_response tests passed!")