# MVP Roadmap

## Current MVP

This runnable MVP implements the documented runtime language directly:
- external agent layer through the adapter interface layer
- simulation runtime core
- four-layer population model

Included runtime modules:
- world engine
- event scheduler
- model router
- memory manager
- semantic cache
- logging hooks suitable for replay and evaluation

## Next Steps

1. Add real external adapters beyond the mock adapter.
2. Introduce richer world policies and cross-agent dependencies.
3. Add replay inspection tools and evaluation metrics.
4. Add budget-aware promotion and demotion across layers.
5. Add benchmark scenarios for cost versus fidelity.
