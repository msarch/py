#version 110

varying vec2 uv;

int max_iter_count;
uniform vec2 C;

int iter_count;
vec2 Z, dZ;
vec2 sqr_Z;
float sqr_norm_Z, sqr_norm_dZ;

void
main() {
	max_iter_count = 1024;
	
	Z = uv; dZ = vec2(1., 0.);
	for(iter_count = 0; iter_count < max_iter_count; ++iter_count) {
		sqr_Z = vec2(Z.x * Z.x, Z.y * Z.y);
		if (sqr_Z.x + sqr_Z.y > 1e7)
			break;

		dZ = vec2(2. * (Z.x * dZ.x - Z.y * dZ.y) + 1., 2. * (Z.x * dZ.y + Z.y * dZ.x));
		Z  = vec2(Z.x * Z.x - Z.y * Z.y, 2. * Z.x * Z.y) + C;
	}

	sqr_norm_Z =   Z.x *  Z.x +  Z.y *  Z.y;
	sqr_norm_dZ = dZ.x * dZ.x + dZ.y * dZ.y;

	
	vec4 color0 = vec4(1.0, 0.0, 0.0, 1.0);
	vec4 color1 = vec4(1.0, 1.0, 0.0, 1.0);
	
	gl_FragColor = mix(color0, color1, sqrt(sqrt(sqr_norm_Z / sqr_norm_dZ) * .5 * log(sqr_norm_Z)));
}

