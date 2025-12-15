#!/usr/bin/env python3
"""
Test script for Multi-Agent Expansion Compression Engine
Demonstrates full model optimization workflow
"""

import asyncio
import json
from src.multi_agent_engine import MultiAgentExpansionCompressionEngine, ModelSize


async def test_multi_agent_engine():
    """Comprehensive test of the multi-agent engine"""

    print("🧪 Testing Multi-Agent Expansion Compression Engine")
    print("=" * 60)

    # Initialize engine
    engine = MultiAgentExpansionCompressionEngine()

    # Test 1: Register multiple models
    print("\n📝 Test 1: Registering Models")
    models = [
        ("tiny_model", "/path/to/tiny", 50_000_000),  # 50M params -> tiny
        ("small_model", "/path/to/small", 300_000_000),  # 300M params -> small
        ("medium_model", "/path/to/medium", 3_000_000_000),  # 3B params -> medium
        ("large_model", "/path/to/large", 30_000_000_000),  # 30B params -> large
    ]

    for model_id, path, params in models:
        initial_metrics = {
            "parameter_count": params,
            "model_size_mb": params * 4 / (1024 * 1024),  # 4 bytes per param
            "inference_time_ms": 100.0,
            "memory_usage_mb": params * 4 / (1024 * 1024),
            "accuracy_score": 0.8,
            "perplexity_score": 20.0,
            "compression_ratio": 1.0,
            "efficiency_score": 1.0,
        }

        model_state = engine.register_model(model_id, path, initial_metrics)
        print(f"  ✅ {model_id}: {model_state.size_category.value} ({params:,} params)")

    # Test 2: Engine status
    print("\n📊 Test 2: Engine Status")
    status = engine.get_engine_status()
    print(json.dumps(status, indent=2))

    # Test 3: Compress large model to medium
    print("\n🗜️ Test 3: Compressing Large Model")
    result = await engine.optimize_model("large_model", ModelSize.MEDIUM)
    print(f"  Operation: {result.get('operation', 'failed')}")
    print(f"  Original size: {result.get('original_size', 'unknown')}")
    print(f"  Target size: {result.get('target_size', 'unknown')}")
    print(f"  Compression steps: {result.get('compression_steps', 0)}")

    # Test 4: Expand tiny model to small
    print("\n📈 Test 4: Expanding Tiny Model")
    result = await engine.optimize_model("tiny_model", ModelSize.SMALL)
    print(f"  Operation: {result.get('operation', 'failed')}")
    print(f"  Original size: {result.get('original_size', 'unknown')}")
    print(f"  Target size: {result.get('target_size', 'unknown')}")
    print(f"  Expansion steps: {result.get('expansion_steps', 0)}")

    # Test 5: Refine medium model for efficiency
    print("\n🔧 Test 5: Refining Medium Model for Efficiency")
    result = await engine.refine_model("medium_model", "efficiency_focused")
    if "error" not in result:
        print("  ✅ Refinement successful")
        print(
            f"  Efficiency improvement: {result.get('efficiency_improvement', 0):.1%}"
        )
    else:
        print(f"  ❌ Refinement failed: {result['error']}")

    # Test 6: Get final model statuses
    print("\n📋 Test 6: Final Model Statuses")
    for model_id in ["tiny_model", "small_model", "medium_model", "large_model"]:
        status = engine.get_model_status(model_id)
        if "error" not in status:
            print(
                f"  {model_id}: {status['size_category']} | {status['current_metrics']['parameter_count']:,} params | {status['compression_history']} compressions | {status['expansion_history']} expansions | {status['refinement_history']} refinements"
            )
        else:
            print(f"  {model_id}: Error - {status['error']}")

    # Test 7: Final engine status
    print("\n🎯 Test 7: Final Engine Status")
    final_status = engine.get_engine_status()
    print(json.dumps(final_status, indent=2))

    print("\n✅ Multi-Agent Engine Test Complete!")


if __name__ == "__main__":
    asyncio.run(test_multi_agent_engine())
