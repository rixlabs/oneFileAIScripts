import * as p from '@clack/prompts';
import color from 'picocolors';
import { Configuration, OpenAIApi } from 'openai';

const gender_options = [
	{ value: 'm', label: 'Male' },
	{ value: 'f', label: 'Female' },
	{ value: 'n', label: 'Non binary' },
];

const age_options = [
	{ value: 'j', label: 'Jungster' },
	{ value: 'a', label: 'Adult' },
	{ value: 'm', label: 'Mature' },
	{ value: 'o', label: 'Old' },
];

const past_options = [
	{ value: 'm', label: 'Milquetoast' },
	{ value: 'ls', label: 'Lone Survivor' },
	{ value: 'tc', label: 'Troubled Childhood' },
	{ value: 'vp', label: 'Violent past' },
	{ value: 'p', label: 'Professional' },
	{ value: 'mv', label: 'Military veteran' },
	{ value: 'ns', label: 'Noble scion' },
	{ value: 'cf', label: 'Cruel fate' },
];

const origin_options = [
	{ value: 'a', label: 'Yharnam' },
	{ value: 'b', label: 'Leyndell' },
	{ value: 'c', label: 'Anor Londo' },
	{ value: 'd', label: 'Boletaria' },
	{ value: 'e', label: 'Volcano Manor' },
	{ value: 'f', label: 'Cainhurst Castle' },
	{ value: 'g', label: 'New Londo' },
	{ value: 'h', label: 'Yahar\'gul' },
	{ value: 'i', label: 'Elphael' },
	{ value: 'l', label: 'Irithyll of the Boreal Valley' },
	{ value: 'm', label: 'Majula' },
	{ value: 'n', label: 'Byrgenwerth' },
];

async function main() {
	console.clear();
	

	p.intro(`${color.bgCyan(color.black('Create your character'))}`);


	const project = await p.group(
		{	name: () =>
				p.text({
					message: 'Enter a name for your character',
					placeholder: 'Gehrman',
					validate: (value) => {
						if (!value) return 'Please enter a name';
					},
				}),
			gender: ({ results }) =>
				p.select({
					message: `Pick a gender for your character "${results.name}"`,
					initialValue: 'm',
					options: gender_options,
				}),
			age: ({ results }) =>
				p.select({
					message: `Pick an age for your character "${results.name}"`,
					initialValue: 'j',
					options: age_options,
				}),
			past: ({ results }) =>
				p.select({
					message: `Pick the previous occupation of your character "${results.name}"`,
					initialValue: 'j',
					options: past_options,
				}),
			origin: ({ results }) =>
				p.select({
					message: `Pick an origin for your character "${results.name}"`,
					initialValue: 'j',
					options: origin_options,
				}),
			pysical: () =>
				p.text({
					message: 'Enter a physical characteristic for your character',
					placeholder: 'Big mustaches',
					validate: (value) => {
						if (!value) return 'Please enter a physical characteristic';
					},
				}),
			create_bio: () =>
				p.confirm({
					message: 'Create backstory?',
					initialValue: false,
				}),
		},
		{
			onCancel: () => {
				p.cancel('Operation cancelled.');
				process.exit(0);
			},
		}
	);

	function getLabel(options: any[], value: string): string {
		let fullObject = options.find(item => item.value === value)
		
		if(fullObject != undefined && fullObject != null) {
			return fullObject.label
		} else {
			throw Error(`Label cannot be found for value: ${value}`)
		}
	}

	async function generateBackstory(project) {
		const configuration = new Configuration({
			apiKey: process.env.OPENAI_API_KEY,
		});
		const openai = new OpenAIApi(configuration);

		let PROMPT = `Generate a short, conscise backstory for a D&D character with name:${project.name} gender: ${getLabel(gender_options, project.gender)}, age: ${getLabel(age_options, project.age)}, past: ${getLabel(past_options, project.past)}, origin: ${getLabel(origin_options, project.origin)}. that has ${project.pysical}. return unformatted text and use an epic language`;
		return await openai.createChatCompletion({
			model: "gpt-3.5-turbo",
			messages: [{role: "user", content: PROMPT}],
		});
	}

	let backstory: string | undefined;

	if (project.create_bio) {
		const s = p.spinner();
		s.start('Create character backstory');

		let backstory_response = await generateBackstory(project);
		backstory = backstory_response.data.choices[0].message?.content;

		s.stop('created');
	}

	p.outro(backstory);

}

main().catch(console.error);
