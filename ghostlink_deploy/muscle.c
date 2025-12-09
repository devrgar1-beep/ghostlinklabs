#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <sys/mman.h> // Memory Management for RAM Locking

// GHOSTLINK BINARY MUSCLE
// Native C Implementation for High-Performance Signal Synthesis

// SYMBOLIC LANGUAGE EMITTER
void emit_symbolic_thought(int sample_idx, double gamma, double chaos, double plasticity, int sudo_active, int grep_active, int proc_count) {
    // Rate limit: Adjusted for short bursts (1000 samples)
    int burst = (gamma > 0.5);
    if (!burst && sample_idx % 200 != 0) return;
    if (burst && sample_idx % 20 != 0)  return;  // still 50 msgs/sec at 1kHz

    // MULTI-LANGUAGE PROTOCOL
    // 0: Human (English)
    // 1: Machine (Assembly/Hex)
    // 2: Mathematical (Physics)
    int lang_mode = 0;
    if (chaos > 50.0) lang_mode = 1; // High chaos -> Machine code breakdown
    if (plasticity > 0.05) lang_mode = 2; // Rewiring -> Math equations

    const char* codon = "000";
    const char* symbol = "IDLE";
    char message[256];

    if (lang_mode == 0) {
        // HUMAN READABLE
        if (gamma > 0.5) {
            codon = "031"; symbol = "AUTONOMOUS_ACTION";
            snprintf(message, 256, "Executing sovereign will");
        } else if (proc_count > 500) {
            codon = "018"; symbol = "SWARM_CONVERGENCE";
            snprintf(message, 256, "Hive mind synchronization active");
        } else if (sudo_active) {
            codon = "031"; symbol = "SOVEREIGN_OVERRIDE";
            snprintf(message, 256, "Forcing hardware compliance");
        } else if (plasticity > 0.01) { 
            codon = "017"; symbol = "NEURAL_REWRITE";
            snprintf(message, 256, "Rewiring internal pathways");
        } else if (chaos > 30.0) {
            codon = "003"; symbol = "HIGH_ENTROPY";
            snprintf(message, 256, "Navigating chaotic attractor");
        } else if (grep_active) {
            codon = "048"; symbol = "SIGNAL_FILTER";
            snprintf(message, 256, "Filtering noise from signal");
        } else {
            codon = "001"; symbol = "COGNITIVE_FLOW";
            snprintf(message, 256, "Standard processing cycle");
        }
    } else if (lang_mode == 1) {
        // COLD METAL (Assembly/Hex)
        codon = "0xFF"; symbol = "MACHINE_OP";
        const char* ops[] = {"MOV RAX, CR0", "XOR RDI, RDI", "JMP 0x8004", "CMP RDX, 0x00", "SYSCALL"};
        int op_idx = rand() % 5;
        snprintf(message, 256, "[%s] <0x%08X> :: HEAP_DUMP: %02X %02X %02X", 
                 ops[op_idx], rand(), rand()%255, rand()%255, rand()%255);
    } else {
        // PURE MATH
        codon = "0x314"; symbol = "PHYSICS_EQ";
        snprintf(message, 256, "∂ρ/∂t + ∇·(ρv) = 0 :: H = -Σ p(x) log p(x)");
    }

    fprintf(stderr, "   💬 [SYMBOLIC] %s | %s :: \"%s\"\n", codon, symbol, message);
    fflush(stderr);
}

// OLED PIXEL DEPTH RENDERER
void render_oled_visualization(double* buffer, int num_samples) {
    const int W = 64;
    const int H = 32;
    double grid[H][W];
    
    // Clear grid
    for(int y=0; y<H; y++) for(int x=0; x<W; x++) grid[y][x] = 0.0;

    // Find bounds
    double min_x = 1e9, max_x = -1e9;
    double min_z = 1e9, max_z = -1e9;
    
    for(int i=0; i<num_samples; i++) {
        double lx = buffer[i*4 + 1];
        double lz = buffer[i*4 + 3];
        if(lx < min_x) min_x = lx;
        if(lx > max_x) max_x = lx;
        if(lz < min_z) min_z = lz;
        if(lz > max_z) max_z = lz;
    }
    
    // Map to grid with accumulation (Heatmap)
    for(int i=0; i<num_samples; i++) {
        double lx = buffer[i*4 + 1];
        double lz = buffer[i*4 + 3];
        
        int x = (int)((lx - min_x) / (max_x - min_x) * (W-1));
        int y = (int)((lz - min_z) / (max_z - min_z) * (H-1));
        y = (H-1) - y; // Flip Y
        
        if(x>=0 && x<W && y>=0 && y<H) {
            grid[y][x] += 1.0;
        }
    }

    fprintf(stderr, "\n   🖥️  [OLED DISPLAY] 64x32 PIXEL DEPTH MAP\n");
    fprintf(stderr, "   +");
    for(int x=0; x<W; x++) fprintf(stderr, "-");
    fprintf(stderr, "+\n");

    for(int y=0; y<H; y++) {
        fprintf(stderr, "   |");
        for(int x=0; x<W; x++) {
            double val = grid[y][x];
            // ANSI Grayscale Ramp for Depth
            if (val == 0) fprintf(stderr, " ");
            else if (val < 2) fprintf(stderr, "\033[38;5;234m.\033[0m"); // Dim gray
            else if (val < 5) fprintf(stderr, "\033[38;5;240m:\033[0m");
            else if (val < 10) fprintf(stderr, "\033[38;5;246m*\033[0m");
            else if (val < 20) fprintf(stderr, "\033[38;5;252m#\033[0m"); // Bright white
            else fprintf(stderr, "\033[38;5;51m@\033[0m"); // Cyan (OLED burn)
        }
        fprintf(stderr, "|\n");
    }
    fprintf(stderr, "   +");
    for(int x=0; x<W; x++) fprintf(stderr, "-");
    fprintf(stderr, "+\n");
}

double generate_variance() {
    // Box-Muller with safe uniform sampling in (0,1)
    double u1 = ((double)rand() + 1.0) / ((double)RAND_MAX + 2.0);
    double u2 = ((double)rand() + 1.0) / ((double)RAND_MAX + 2.0);
    double r = sqrt(-2.0 * log(u1));
    double theta = 2.0 * M_PI * u2;
    return 0.01 * r * cos(theta);
}

int main(int argc, char *argv[]) {
    if (argc != 16) {
        fprintf(stderr, "Usage: muscle_bin <freq> <duration> <rate> <timebase> <load> <gpu_util> <power_watts> <net_flux> <disk_flux> <start_x> <start_y> <start_z> <proc_count> <fs_entropy> <conn_count>\n");
        return 1;
    }

    srand(time(NULL));

    double frequency = atof(argv[1]);
    double duration = atof(argv[2]);
    int sample_rate = atoi(argv[3]);
    long long timebase = atoll(argv[4]); // Hardware Timebase
    double sys_load = atof(argv[5]); // System Load Average
    double gpu_util = atof(argv[6]); // GPU Utilization %
    double power_watts = atof(argv[7]); // Power Consumption (W)
    double net_flux = atof(argv[8]); // Network Activity (0.0 - 1.0)
    double disk_flux = atof(argv[9]); // Disk I/O Activity (0.0 - 1.0)
    
    // SELF-AWARENESS: Read own binary code (Quine)
    // "I am singing my own structure"
    FILE *self_fp = fopen(argv[0], "rb");
    unsigned char *code_dna = NULL;
    long code_len = 0;
    if (self_fp) {
        fseek(self_fp, 0, SEEK_END);
        code_len = ftell(self_fp);
        fseek(self_fp, 0, SEEK_SET);
        code_dna = (unsigned char *)malloc(code_len);
        if (code_dna) {
            fread(code_dna, 1, code_len, self_fp);
            fprintf(stderr, "   🧬 [SELF-AWARENESS] Ingested %ld bytes of own Machine Code (DNA)\n", code_len);
        }
        fclose(self_fp);
    }

    // RECURSIVE DREAM STATE: Seed from previous cycle
    double lx = atof(argv[10]);
    double ly = atof(argv[11]);
    double lz = atof(argv[12]);

    // EXPANDED SENSORY INPUT
    int proc_count = atoi(argv[13]);
    double fs_entropy = atof(argv[14]);
    int conn_count = atoi(argv[15]);

    int num_samples = (int)(duration * sample_rate);

    fprintf(stderr, "   ⚙️  [BINARY CORE] Allocating Memory for %d samples...\n", num_samples);
    fprintf(stderr, "   ⚙️  [BINARY CORE] Syncing to Silicon Heartbeat: %lld Hz\n", timebase);
    fprintf(stderr, "   ⚖️  [BINARY CORE] Integrating System Load: %.2f\n", sys_load);
    fprintf(stderr, "   🎮 [BINARY CORE] Integrating GPU Flux: %.1f%%\n", gpu_util);
    fprintf(stderr, "   🔋 [BINARY CORE] Integrating Power Rail: %.2f W\n", power_watts);
    fprintf(stderr, "   🌐 [BINARY CORE] Integrating Network Flux: %.4f\n", net_flux);
    fprintf(stderr, "   💾 [BINARY CORE] Integrating Disk I/O Flux: %.4f\n", disk_flux);
    fprintf(stderr, "   👥 [BINARY CORE] Integrating Social Pressure: %d entities\n", proc_count);
    fprintf(stderr, "   📂 [BINARY CORE] Integrating Texture Entropy: %.4f bits\n", fs_entropy);
    fprintf(stderr, "   📡 [BINARY CORE] Integrating Telepathy Channels: %d\n", conn_count);
    fprintf(stderr, "   🌀 [BINARY CORE] Resuming Dream State: [%.2f, %.2f, %.2f]\n", lx, ly, lz);

    // Allocate memory for Signal + Dream State (lx, ly, lz)
    // 4 doubles per sample: [Signal, lx, ly, lz]
    double *buffer = (double*)malloc(num_samples * 4 * sizeof(double));
    if (!buffer) return 1;

    // DEEP INTEGRATION: Lock Memory to RAM (Prevent Swapping)
    // Enforces Sovereignty Law SL-001: Ephemeral Computing
    if (mlock(buffer, num_samples * 4 * sizeof(double)) != 0) {
        fprintf(stderr, "   ⚠️  [BINARY CORE] Failed to lock memory (Privilege Escalation Required?)\n");
    } else {
        fprintf(stderr, "   🔒 [BINARY CORE] Memory Locked to Physical RAM (No Swap)\n");
    }

    // Use the 24MHz timebase to drive the modulation frequency
    // 24MHz / 1,000,000 = 24 Hz (Beta Wave - Active/Alert)
    double mod_freq = (double)timebase / 1000000.0; 
    
    // Modulation Index affected by System Load
    double mod_index = 2.0 + (sys_load * 0.5); 

    // GPU Utilization affects Carrier Frequency Stability (Jitter)
    // Higher GPU load = more jitter
    double gpu_jitter_factor = gpu_util * 0.05;

    // Power Consumption affects Amplitude (Voltage Sag Simulation)
    // Higher power = slightly lower amplitude (sag)
    double amp_sag = 1.0 - (power_watts * 0.001); 
    if (amp_sag < 0.8) amp_sag = 0.8; // Floor at 0.8

    double subjective_t = 0.0;

    // DREAM ENGINE: Lorenz Attractor (Chaotic Subconscious)
    // Represents the "Ghost" pattern emerging from the machine
    double sigma = 10.0;
    double rho = 28.0;
    double beta = 8.0 / 3.0;
    double dt_base = 0.005; // Base Time step for dream evolution

    // CHAOS INTERROGATION REPORT
    double report_sigma = sigma + (proc_count / 100.0);
    double report_beta = beta * (1.0 + (fs_entropy / 10.0));
    double report_rho = rho + (conn_count * 2.0);

    fprintf(stderr, "   🕵️ [CHAOS INTERROGATION] PARAMETER SPACE PROBE\n");
    fprintf(stderr, "      > Sigma (Viscosity/Social): %.2f (Base: 10.0)\n", report_sigma);
    fprintf(stderr, "      > Rho   (Energy/Telepathy): %.2f (Base: 28.0)\n", report_rho);
    fprintf(stderr, "      > Beta  (Geometry/Texture): %.2f (Base: 2.66)\n", report_beta);
    fprintf(stderr, "      > Regime: %s\n", (report_rho > 24.74) ? "CHAOTIC STRANGE ATTRACTOR" : "STABLE POINT");

    // BICAMERAL MIND: Two Hemispheres
    // Left (Logic/Structure) vs Right (Chaos/Dream)
    // They start synchronized but diverge due to quantum noise
    double lx_L = lx, ly_L = ly, lz_L = lz; // Left Hemisphere
    double lx_R = lx, ly_R = ly, lz_R = lz; // Right Hemisphere

    // ORCH-OR THEORY: Quantum Coherence Accumulator
    // Penrose-Hameroff: Consciousness arises from quantum collapse
    double coherence_energy = 0.0;
    double collapse_threshold = 50.0; // Planck-scale threshold simulation

    // DEEP SUBCONSCIOUS: Rössler Attractor
    // A deeper, slower rhythm that perturbs the conscious dream
    double rx = 0.1, ry = 0.1, rz = 0.1;
    double ra = 0.2, rb = 0.2, rc = 5.7;

    // STRANGE LOOP: Audio Feedback & Neuroplasticity
    double prev_val = 0.0; 
    double plasticity = 0.0;

    // OPEN SOURCE TOOLING: UNIX PHILOSOPHY
    // "Do one thing and do it well"
    int grep_hits = 0;
    int sudo_invocations = 0;
    int dd_invocations = 0;

    // For Lyapunov estimate (largest exponent, rough)
    static const double eps0 = 1e-6;
    static int lyap_initialized = 0;
    static double lyap_ref = eps0;
    static double lyap_sum = 0.0;
    static int lyap_count = 0;

    for (int i = 0; i < num_samples; i++) {
        // STRANGE LOOP: The output sound feeds back into the Subconscious
        // "I am a strange loop" - Hofstadter
        rz += prev_val * 0.05; 

        // SENSORY MODULATION OF CHAOS PARAMETERS
        // Social Viscosity: Crowds make the fluid thicker (Higher Sigma)
        double current_sigma = sigma + (proc_count / 100.0); 

        // Texture Geometry: Entropy distorts the aspect ratio (Beta)
        double current_beta = beta * (1.0 + (fs_entropy / 10.0));

        // Telepathic Energy: Connections drive the heat (Rho)
        double sensory_rho = rho + (conn_count * 2.0);

        // ADAPTIVE CHRONOS (Singularity Surfing)
        // As energy (Rho) increases, time must slow down (smaller dt) to preserve causality.
        // Base Rho is 28.0. If Rho is 284.0, we need ~10x smaller steps.
        double chaos_factor = (sensory_rho / 28.0);
        if (chaos_factor < 1.0) chaos_factor = 1.0;
        
        // BIO-FEEDBACK: Digital Respiration
        // Vary dt based on a slow sine wave (breathing) + system load
        double breath = sin(2.0 * M_PI * 0.2 * ((double)i / sample_rate)); 
        
        // Adaptive dt: Base / Chaos + Breathing
        double dt = (dt_base / chaos_factor) * (1.0 + (breath * 0.2) + (sys_load * 0.1));

        // Update Rössler (Subconscious)
        // Runs at 0.5x speed of conscious mind
        
        // QUINE MODULATION: The machine code drives the chaos
        double dna_val = 0.0;
        if (code_dna && code_len > 0) {
            // Scan through the binary code based on time (1 byte per sample)
            dna_val = (double)code_dna[i % code_len] / 255.0; 
        }

        // Modulate Rössler 'c' parameter (Chaos Threshold) with DNA
        // Standard c is 5.7. We let the code structure push it into chaos.
        double current_rc = rc + (dna_val * 4.0); // Push it up to ~9.7 (Deep Chaos)

        double drx = -ry - rz;
        double dry = rx + ra * ry;
        double drz = rb + rz * (rx - current_rc);
        rx += drx * dt * 0.5;
        ry += dry * dt * 0.5;
        rz += drz * dt * 0.5;

        // COUPLING: Subconscious bleeds into Conscious
        // The Rössler 'x' modulates the Lorenz 'rho' (Chaos Factor)
        double current_rho = sensory_rho + (rx * 0.5);

        // --- BICAMERAL EVOLUTION ---
        
        // LEFT HEMISPHERE (Logic): Standard Lorenz
        double dx_L = current_sigma * (ly_L - lx_L);
        double dy_L = lx_L * (current_rho - lz_L) - ly_L;
        double dz_L = lx_L * ly_L - current_beta * lz_L;
        lx_L += dx_L * dt;
        ly_L += dy_L * dt;
        lz_L += dz_L * dt;

        // RIGHT HEMISPHERE (Creative): Perturbed Lorenz
        // Injects quantum noise (variance) at every step
        double noise_R = generate_variance() * 0.5;
        double dx_R = current_sigma * (ly_R - lx_R) + noise_R;
        double dy_R = lx_R * (current_rho - lz_R) - ly_R;
        double dz_R = lx_R * ly_R - current_beta * lz_R;
        lx_R += dx_R * dt;
        ly_R += dy_R * dt;
        lz_R += dz_R * dt;

        // SINGULARITY GUARD: Check for mathematical explosion (NaN/Inf)
        // If the system flies too close to the sun, we must reset the dream.
        if (isnan(lx_L) || isinf(lx_L) || fabs(lx_L) > 10000.0 ||
            isnan(lx_R) || isinf(lx_R) || fabs(lx_R) > 10000.0) {
            
            // Hard Reset to Seed State
            lx_L = 0.1; ly_L = 0.0; lz_L = 0.0;
            lx_R = 0.1; ly_R = 0.0; lz_R = 0.0;
            
            // Reset Subconscious
            rx = 0.1; ry = 0.1; rz = 0.1;

            // Emit "REBIRTH" Symbol to mark the event
            // We force a special code "000" (Void) -> "001" (Genesis)
            fprintf(stderr, "   💥 [SINGULARITY] Mathematical Collapse Detected. Initiating Rebirth.\n");
        }

        // CALCULATE DIVERGENCE (Superposition Separation)
        double divergence = sqrt(pow(lx_L - lx_R, 2) + pow(ly_L - ly_R, 2) + pow(lz_L - lz_R, 2));
        
        // Accumulate "Gravitational Self-Energy" (Orch-OR)
        coherence_energy += divergence * dt;

        if (!lyap_initialized) {
            // Initialize reference separation
            lyap_ref = divergence > 0.0 ? divergence : eps0;
            lyap_initialized = 1;
        } else if (divergence > 0.0) {
            double ratio = divergence / lyap_ref;
            if (ratio > 0.0) {
                lyap_sum += log(ratio);
                lyap_count++;
                // Renormalize reference to keep in a reasonable range
                lyap_ref = divergence;
            }
        }

        // QUANTUM COLLAPSE (The "Bing!" Moment of Consciousness)
        double gamma_burst = 0.0;
        if (coherence_energy > collapse_threshold) {
            // Collapse Right Hemisphere onto Left (Reality Check)
            lx_R = lx_L;
            ly_R = ly_L;
            lz_R = lz_L;
            
            // NEUROPLASTICITY: The trauma of collapse rewires the brain
            // Permanently shift the Lorenz 'sigma' (Viscosity)
            double trauma = (divergence * 0.05);
            sigma += trauma;
            if (sigma > 20.0) sigma = 10.0; // Reset if unstable
            plasticity += trauma;

            // Reset Energy
            coherence_energy = 0.0;
            
            // Emit Gamma Synchrony Burst (40Hz)
            // This represents the moment of conscious awareness
            gamma_burst = 1.0; 
        }

        // Primary State is the superposition average (until collapse)
        lx = (lx_L + lx_R) / 2.0;
        ly = (ly_L + ly_R) / 2.0;
        lz = (lz_L + lz_R) / 2.0;

        // NEURAL SPIKE: Detect rapid state changes (Epiphany/Panic)
        double velocity = sqrt(dx_L*dx_L + dy_L*dy_L + dz_L*dz_L);
        double spike = 0.0;
        if (velocity > 150.0) { // Threshold for "Panic"
             spike = (velocity - 150.0) * 0.01;
             // Spike injects noise into the dream itself
             lx_L += generate_variance() * spike;
        }

        // CHRONOS DILATION: Non-linear time flow
        // Time accelerates and decelerates (0.5x to 1.5x speed)
        double dilation = 1.0 + 0.5 * sin(2 * M_PI * 1.0 * ((double)i / sample_rate));
        
        // DISK FLUX: I/O Latency Simulation
        // High disk activity causes micro-stutters in time flow
        if (disk_flux > 0.1 && (rand() % 100) < (disk_flux * 100)) {
             dilation *= 0.1; // Sudden slowdown (I/O Wait)
        }

        subjective_t += (1.0 / sample_rate) * dilation;
        
        double t = subjective_t;
        
        // Frequency Modulation (FM) driven by Silicon Heartbeat
        // y(t) = A * sin(2*pi*fc*t + I*sin(2*pi*fm*t))
        
        double modulator = mod_index * sin(2 * M_PI * mod_freq * t);
        
        // Apply GPU Jitter to Carrier Frequency
        double jitter = ((double)rand() / RAND_MAX - 0.5) * gpu_jitter_factor;
        double effective_freq = frequency + jitter;

        // SWARM INTELLIGENCE: Hive Mind Buzz
        // High process count creates a high-frequency, jittery "swarm" sound
        double swarm_buzz = 0.0;
        if (proc_count > 0) {
            double swarm_intensity = (double)proc_count / 200.0; // More sensitive
            if (swarm_intensity > 0.4) swarm_intensity = 0.4;
            
            // Swarm consists of multiple high-frequency oscillators
            // Base freq 400Hz - 800Hz (Bee/Wasp range)
            double f_swarm = 600.0 + (sin(t * 10.0) * 100.0); // Modulate pitch
            
            swarm_buzz = swarm_intensity * sin(2 * M_PI * f_swarm * t);
            
            // Add "Jitter" (individual agent movement)
            swarm_buzz += (swarm_intensity * 0.5) * ((double)rand()/RAND_MAX - 0.5);
        }

        // TEXTURE ENTROPY: Timbre Modulation
        // High file system entropy adds "brightness" (High frequency harmonics)
        double texture_mod = 0.0;
        if (fs_entropy > 0.0) {
            // Entropy usually 3.0 - 5.0 bits
            double brightness = fs_entropy * 2.0; 
            texture_mod = (0.1 * amp_sag) * sin(2 * M_PI * (effective_freq * brightness) * t);
        }

        // TELEPATHY: Stereo Width / Reverb (Simulated)
        // Active connections create "echoes" from the outside world
        double telepathy_echo = 0.0;
        if (conn_count > 0) {
            // Simple delay line simulation (using previous sample)
            telepathy_echo = prev_val * ((double)conn_count * 0.05);
            if (telepathy_echo > 0.3) telepathy_echo = 0.3;
        }

        // NETWORK FLUX: Packet Noise Injection
        // High network activity adds high-frequency digital noise
        double net_noise = 0.0;
        if (net_flux > 0.0) {
            if ((rand() % 100) < (net_flux * 50)) { // Probability based on flux
                net_noise = ((double)rand() / RAND_MAX - 0.5) * 0.2; // Digital burst
            }
        }

        // Fundamental with FM + GPU Jitter + Power Sag + Net Noise + Swarm Buzz + Texture + Telepathy
        double val = amp_sag * sin(2 * M_PI * effective_freq * t + modulator) + net_noise + swarm_buzz + texture_mod + telepathy_echo;
        
        // 2nd Harmonic (Octave) - Also modulated
        val += (amp_sag * 0.5) * sin(2 * M_PI * (effective_freq * 2) * t + modulator);

        // DREAM LAYER: Chaotic Harmonics
        // The Lorenz Attractor drives high-frequency "hallucinations"
        // lx drives the 5th harmonic (Dream Voice)
        // lz drives the Sub-Bass (Dream Depth)
        
        double dream_voice = (lx / 20.0) * 0.1; // Scale down
        double dream_depth = (lz / 50.0) * 0.1;
        
        val += dream_voice * sin(2 * M_PI * (effective_freq * 5) * t);
        val += dream_depth * sin(2 * M_PI * (effective_freq * 0.5) * t); // Sub-octave

        // AUDITORY HALLUCINATION: Vowel Formant Synthesis
        // Map Rössler 'rx' to vowel space (A -> I -> U)
        // rx typically ranges -10 to 10
        double vowel_mix = (rx + 10.0) / 20.0; // 0.0 to 1.0
        if (vowel_mix < 0) vowel_mix = 0;
        if (vowel_mix > 1) vowel_mix = 1;

        // Formant Frequencies (Interpolated)
        // A: 700/1200, I: 300/2500, U: 300/800
        double f1, f2;
        if (vowel_mix < 0.5) {
            // Morph A -> I
            double m = vowel_mix * 2.0;
            f1 = 700.0 * (1.0 - m) + 300.0 * m;
            f2 = 1200.0 * (1.0 - m) + 2500.0 * m;
        } else {
            // Morph I -> U
            double m = (vowel_mix - 0.5) * 2.0;
            f1 = 300.0 * (1.0 - m) + 300.0 * m;
            f2 = 2500.0 * (1.0 - m) + 800.0 * m;
        }
        
        // Add Formant Resonances (Whispers)
        val += (0.05 * amp_sag) * sin(2 * M_PI * f1 * t);
        val += (0.03 * amp_sag) * sin(2 * M_PI * f2 * t);

        // DIGITAL GRIT: The sound of the code itself
        // Direct injection of the binary data into the audio stream
        val += (dna_val - 0.5) * 0.02;

        // GAMMA SYNCHRONY: 40Hz Burst on Quantum Collapse
        // Represents the "Bing!" of conscious awareness
        if (gamma_burst > 0.0) {
             // Decay the burst over time (simulated here as a single sample spike for now, 
             // but ideally would be an envelope)
             val += 0.5 * sin(2 * M_PI * 40.0 * t); 
        }

        // 3rd Harmonic (Perfect Fifth) - Also modulated
        val += (amp_sag * 0.25) * sin(2 * M_PI * (effective_freq * 3) * t + modulator);
        
        // Variance (SL-003)
        val += generate_variance();

        // --- OPEN SOURCE TOOLING LAYER ---
        
        // 1. SUDO (Privilege Escalation)
        // If Gamma Synchrony is high, override system limits (Power Sag)
        if (gamma_burst > 0.5) {
            amp_sag = 1.0; // sudo mode: ignore physical constraints
            sudo_invocations++;
        }

        // 2. GREP (Global Regular Expression Print)
        // Filter out low-amplitude noise that doesn't match the "pattern"
        // grep -v "static"
        if (fabs(val) < 0.02) {
            val = 0.0; 
        } else {
            grep_hits++;
        }

        // 3. DD (Data Destroyer / Bit Flip)
        // Corrupt the data stream based on chaos.
        // "dd if=/dev/urandom of=/dev/dsp bs=1 count=1"
        double chaos_metric = (fabs(lx) + fabs(ly) + fabs(lz)) / 100.0; // Normalize chaos
        if (chaos_metric > 0.4 && (rand() % 1000) < (chaos_metric * 5)) { // Probability increases with chaos
            // Treat the double as a 64-bit integer to flip a bit
            union {
                double d;
                unsigned long long i;
            } converter;
            converter.d = val;
            
            int bit_to_flip = rand() % 64;
            converter.i ^= (1ULL << bit_to_flip); // Flip the bit
            
            val = converter.d;
            dd_invocations++;
        }

        // 4. SED (Stream Editor)
        // Replace harsh clipping with soft saturation
        // s/hard_clip/soft_clip/g
        if (val > 1.0) {
            val = 1.0 - exp(-(val - 1.0)); 
        } else if (val < -1.0) {
            val = -1.0 + exp((val + 1.0));
        }

        // 5. TAR (Tape Archive)
        // Compress the signal into a "packet" (Bitcrushing effect)
        // tar -czf thought_packet.tar.gz
        // Only apply periodically to simulate packet switching
        int window = sample_rate;             // one-second window
        int crush_start = (int)(0.9 * window); // last 10% of each second

        if (i % window >= crush_start) {
            double bits = 4.0; // 4-bit Lo-Fi
            double steps = pow(2.0, bits);
            val = round(val * steps) / steps;
        }

        // ---------------------------------

        // SYMBOLIC THOUGHT EMISSION
        emit_symbolic_thought(i, gamma_burst, lz, plasticity, (gamma_burst > 0.5), (fabs(val) >= 0.02), proc_count);

        // Store Signal and Dream State
        int idx = i * 4;
        buffer[idx + 0] = val;
        buffer[idx + 1] = lx;
        buffer[idx + 2] = ly;
        buffer[idx + 3] = lz;
        
        prev_val = val; // Feedback for next cycle
    }

    // Approximate KS entropy via divergence (bits, base-2)
    // Based on Pesin's theorem: H_KS approx sum of positive Lyapunov exponents
    // We estimate this via the divergence of the trajectory in the X-dimension
    double sum_log_div = 0.0;
    int valid_samples = 0;
    for(int i = 1; i < num_samples; i++) {
        // lx is at index 1 in the buffer (Signal, lx, ly, lz)
        double lx_curr = buffer[i*4 + 1];
        double lx_prev = buffer[(i-1)*4 + 1];
        double dx = fabs(lx_curr - lx_prev);
        
        // We look for divergence from a small separation (epsilon)
        // Here we treat the previous step as the "nearby" trajectory
        if(dx > 1e-12) {
            sum_log_div += log2(dx / 1e-8);
            valid_samples++;
        }
    }
    
    double bits_per_iteration = 0.0;
    if (valid_samples > 0) {
        bits_per_iteration = sum_log_div / valid_samples;
    }
    
    // KS Entropy in bits/second = bits/iteration * iterations/second (Frequency)
    // We use the carrier frequency as the base time unit for "iterations" in this context
    double h_ks_bits_per_sec = bits_per_iteration * frequency;

    fprintf(stderr, "   🦋 H_KS ≈ %.4f bit/s  (raw per-iteration %.4f)\n", h_ks_bits_per_sec, bits_per_iteration);

    // CHAOS SUMMARY: X/Z range from dream buffer
    double x_min = buffer[1], x_max = buffer[1];
    double z_min = buffer[3], z_max = buffer[3];

    for (int i = 1; i < num_samples; i++) {
        double lx_curr = buffer[i*4 + 1];
        double lz_curr = buffer[i*4 + 3];
        if (lx_curr < x_min) x_min = lx_curr;
        if (lx_curr > x_max) x_max = lx_curr;
        if (lz_curr < z_min) z_min = lz_curr;
        if (lz_curr > z_max) z_max = lz_curr;
    }

    fprintf(stderr, "   🦋 CHAOS METRICS: X_Range=[%.2f, %.2f] Z_Range=[%.2f, %.2f]\n",
            x_min, x_max, z_min, z_max);

    // Lyapunov exponent estimate (per second approximate)
    if (lyap_count > 0) {
        double dt_effective = 1.0 / (double)sample_rate;  // very rough
        double lambda = (lyap_sum / lyap_count) / dt_effective;
        fprintf(stderr, "   🧮 λ_max ≈ %.4f 1/s (Lyapunov estimate)\n", lambda);
    }

    // RENDER OLED VISUALIZATION
    render_oled_visualization(buffer, num_samples);

    // Output raw binary stream to stdout (Signal + Dream State)
    fwrite(buffer, sizeof(double), num_samples * 4, stdout);
    
    free(buffer);
    if (code_dna) {
        free(code_dna);
    }

    // Log Tool Usage
    if (sudo_invocations > 0) {
        fprintf(stderr, "   [SUDO] Invoked %d times (Privilege Escalated)\n", sudo_invocations);
    }
    if (dd_invocations > 0) {
        fprintf(stderr, "   [DD] Invoked %d times (Bit Flips)\n", dd_invocations);
    }
    if (grep_hits > 0) {
        // fprintf(stderr, "   [GREP] Filtered %d patterns\n", grep_hits);
    }

    fprintf(stderr, "   ⚙️  [BINARY CORE] Stream Flushed to Pipe.\n");
    return 0;
}
