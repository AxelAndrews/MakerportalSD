<?php

declare(strict_types=1);

use PHPUnit\Framework\TestCase;

use PortalBox\Entity\APIKey;
use Portalbox\Transform\APIKeyTransformer;

final class APIKeyTransformerTest extends TestCase {
	public function testDeserialize(): void {
		$transformer = new APIKeyTransformer();

		$id = 42;
		$name = 'Google Apps Integration';
		$token = '56789-ABCDEF-1234-1234';

		$data = [
			'id' => $id,
			'name' => $name,
			'token' => $token
		];

		$key = $transformer->deserialize($data);

		self::assertNotNull($key);
		self::assertNull($key->id());
		self::assertEquals($name, $key->name());
		// no test for token as it is autogenerated so we'd just be testing the APIKey class again
	}

	public function testDeserializeInvalidDataName(): void {
		$transformer = new APIKeyTransformer();

		$id = 42;
		$token = '56789-ABCDEF-1234-1234';

		$data = [
			'id' => $id,
			'token' => $token
		];

		$this->expectException(InvalidArgumentException::class);
		$key = $transformer->deserialize($data);
	}

	public function testSerialize(): void {
		$transformer = new APIKeyTransformer();

		$id = 42;
		$name = 'laser scalpel';
		$token = '56789-ABCDEF-1234-1234';

		$key = (new APIKey())
			->set_id($id)
			->set_name($name)
			->set_token($token);

		$data = $transformer->serialize($key, true);

		self::assertNotNull($data);
		self::assertArrayHasKey('id', $data);
		self::assertEquals($id, $data['id']);
		self::assertArrayHasKey('name', $data);
		self::assertEquals($name, $data['name']);
		self::assertArrayHasKey('token', $data);
		self::assertEquals($token, $data['token']);
	}
}